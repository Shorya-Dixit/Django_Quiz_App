$(document).ready(function() {
    let currentQuestionIndex = 0;
    let quizData = [];

    // Fetch the first question when the quiz starts
    fetchQuestion();

    function fetchQuestion() {
        $.get("/quiz/question/", function(data) {
            if (data.error) {
                alert(data.error);
                return;
            }
            
            const question = data.question;
            const options = data.options;
            
            // Update the question text
            $('#question-text').text(question);

            // Clear existing options
            $('#options-container').empty();

            // Add options as buttons
            options.forEach(function(option, index) {
                $('#options-container').append(`
                    <button class="option-btn" data-index="${index}">${option}</button>
                `);
            });

            // Show the submit button
            $('#submit-btn').show();
            $('#next-btn').hide();
        });
    }

    // Submit the answer for the current question
    $('#submit-btn').click(function() {
        const userAnswer = $("button.option-btn.selected").data("index");

        if (userAnswer === undefined) {
            alert("Please select an answer.");
            return;
        }

        $.post("/quiz/submit/", { answer: userAnswer }, function(data) {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Show next question button
            $('#next-btn').show();
            $('#submit-btn').hide();

            if (data.next_action === "summary") {
                showSummary();
            }
        });
    });

    // When the "Next" button is clicked, fetch the next question
    $('#next-btn').click(function() {
        fetchQuestion();
    });

    // Select an answer when the option button is clicked
    $('#options-container').on('click', '.option-btn', function() {
        $(".option-btn").removeClass('selected');
        $(this).addClass('selected');
    });

    // Show the quiz summary after completion
    function showSummary() {
        $.get("/quiz/summary/", function(data) {
            if (data.error) {
                alert(data.error);
                return;
            }

            $('#quiz-container').hide();
            $('#summary-container').show();

            const summaryAnswers = data.answers;
            const totalQuestions = data.total_questions;

            summaryAnswers.forEach(function(answer, index) {
                const isCorrect = answer.is_correct ? "Correct" : "Incorrect";
                $('#summary-answers').append(`
                    <li>
                        Question ${index + 1}: ${answer.question}<br>
                        Your Answer: ${answer.options[answer.user_answer]}<br>
                        Correct Answer: ${answer.options[answer.correct_answer]}<br>
                        <b>${isCorrect}</b>
                    </li>
                `);
            });

            $('#summary-answers').append(`
                <li>Total Correct Answers: ${data.correct_answers} / ${totalQuestions}</li>
                <li>Total Incorrect Answers: ${data.incorrect_answers} / ${totalQuestions}</li>
            `);
        });
    }
});
