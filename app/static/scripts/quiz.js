/* globals jQuery, $ */

$(document).ready(function(){

    var previousInputsList = [],
        correctAnswerCount = 0,
        tagCount = $('meta[name="tag-count"]').attr('value'),
        showAllButton = $("#show-all"),
        input = $("input"),
        tagList = null;

        $("[name=enter-input]").click(checkTagName);
        showAllButton.click(showRest);
        input.keyup(keyUpHandler);
        $('#valid-tags, #still-to-learn').on("click","tr.tag-name", toggleDefinitionRow);
        $('#retry').click(function() {
            window.location.reload(true);
        });
        
        // prevent page reload when submitting answer
        $("form").submit(function() {
            return false;
        });



        function checkTagName() {
            var userInput = filterInput(),
                tagObj =  {
                    name: userInput.tagName,
                    definition: null
                };

            clearInput();
            input.attr('disabled', 'disabled').attr('placeholder', 'Checking your answer now.');
            
            $.ajax({
                url: 'api/v1.0/definition',
                data: {'tagname': tagObj.name},
                dataType: 'json',
                type: 'GET',
                success: function(data) {
                    definition = data.definition;

                    if (definition) {

                        tagObj.definition = definition;
                        $("#valid-tags tbody").append($("#new-row").template({tag: tagObj}));

                        correctAnswerCount += 1;
                        updateCorrectAnswerCountIndicator();
                        logInput(userInput.tagName);
                        showSuccess();

                        if (correctAnswerCount === tagCount) {
                            displayCongratulations();
                        }

                    } else {
                        $("#invalid-tags tbody").append($("#new-row").template({tag: tagObj}));
                        logInput(userInput.wholeText);
                        showFailure();
                    }

                },
                complete: function() {
                    input.removeAttr('disabled').attr('placeholder', 'Enter tag names here').focus();    
                }
            });
        }

        function filterInput() {
            var inputFilter = /^(\S+)(\s*(.*))$/,
                inputs = inputFilter.exec(input.val().trim()); 
            
            return {
                tagName: inputs[0],
                wholeText: inputs[2]
            };
        }
        
        function clearInput() {
            input.val("");
            $("[name=enter-input]").attr("disabled", "disabled");
        }

        function updateCorrectAnswerCountIndicator() {
            $("#tags-left").html(115 - correctAnswerCount);
        }

        function showSuccess() {
            $("#failure").hide();
            $("#success").show();
        }

        function showFailure() {
            $("#success").hide();
            $("#failure").show();
        }

        function displayCongratulations() {
            $('form.form-group').replaceWith('<div class="col-sm-12 text-center"><strong>Congratulations!' + 
                '</strong> You remembered all of the valid HTML5 tag names!</div>');
        }

        function logInput(input) {
            previousInputsList.push(input);
        }



        // checks if input text has already been given as an answer and 
        // checks tag name when Return is pressed
        function keyUpHandler() {
            var inputValue = $(this).val().trim(),
                prompt = $("#already-answered-prompt"),
                button = $("[name=enter-input]");

            hideSuccessFailure();

            if (inputValue) {
                if ($.inArray(inputValue, previousInputsList) > -1) {
                    prompt.removeClass("invisible");
                    button.attr("disabled", "disabled");
                } else {
                    prompt.addClass("invisible");
                    button.removeAttr("disabled");
                    
                    //when user presses 'Return'
                    if (event.keyCode === 13) {
                        checkTagName();
                    }
                }
            } else {
                prompt.addClass("invisible");
                button.attr("disabled", "disabled");
            }
        }

        function hideSuccessFailure() {
            $("#success, #failure").hide()
        }




        function showRest() {

            $.ajax({
                url: '/api/v1.0/remaining_tags',
                data: { 'answered': previousInputsList },
                traditional: true,
                success: function(data) {
                    for (var key in data) {
                        var newItem = $("#new-row").template({
                            tag: {
                                name: key,
                                definition: data[key]
                            }
                        }).filter("*");
                        $("#still-to-learn tbody").append(newItem);
                    }

                    showAllButton.attr("disabled", "disabled");
                    $("input").attr("disabled", "disabled");
               
                    clearInput();     
                    hideSuccessFailure();
                    showResults();
                    switchToRetry();
                }
            });
        }

        function showResults() {
            var elem = "<p class='text-center margin-top-small'><strong>You remembered " + 
                correctAnswerCount + " out of " + tagCount + " tag names!</strong></p>";
            $(".form-group.icon-add-on").find("p").remove();
            $(".form-group.icon-add-on").append(elem);
        }

        function switchToRetry() {
            $('#retry').show();
            $('#show-all').hide();
        }



        function toggleDefinitionRow() {
            $(this).toggleClass("active-cell");
            $(this).next().toggle();
        }
});