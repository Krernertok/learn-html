$(document).ready(function(){

    var previousInputs = [],
        correctAnswers = 0,
        tagCount = $('meta[name="tag-count"]').attr('value'),
        showAllButton = $("#show-all"),
        input = $("input"),
        tagList = null,
        
        checkTagName = function() {
            var userInput = filterInput(),
                tag =  {
                    name: userInput.tagName,
                    definition: null
                };

            clearInput();
            input.attr('disabled', 'disabled').attr('placeholder', 'Checking your answer now.');
            
            $.ajax({
                url: 'api/v1.0/definition',
                data: {'tagname': tag.name},
                dataType: 'json',
                type: 'GET',
                success: function(data) {
                    definition = data.definition;

                    if (definition) {

                        tag.definition = definition;
            
                        correctAnswers += 1;
                        updateCorrectAnswersIndicator();
                        showSuccess();
                        
                        logInput(userInput.tagName);            
                        $("#valid-tags tbody").append($("#new-row").template({tag: tag}));

                        if (correctAnswers === tagCount) {
                            displayCongratulations();
                        }

                    } else {
                        logInput(userInput.wholeText);
                        showFailure();
                        $("#invalid-tags tbody").append($("#new-row").template({tag: tag}));
                    }

                },
                complete: function() {
                    input.removeAttr('disabled').attr('placeholder', 'Enter tag names here').focus();    
                }
            });
        },
        
        clearInput = function() {
            input.val("");
            $("[name=enter-input]").attr("disabled", "disabled");
        },

        displayCongratulations = function() {
            $('form.form-group').replaceWith('<div class="col-sm-12 text-center"><strong>Congratulations!' + 
                '</strong> You remembered all of the valid HTML5 tag names!</div>');
        },

        filterInput = function() {
            var inputFilter = /^(\S+)(\s*(.*))$/,
                inputs = inputFilter.exec(input.val().trim()); 
            
            return {
                tagName: inputs[0],
                wholeText: inputs[2]
            };
        },

        hideSuccessFailure = function() {
            $("#success, #failure").hide()
        },
        
        keyUpHandler = function(event) {
            var inputValue = $(this).val().trim(),
                prompt = $("#already-answered-prompt"),
                button = $("[name=enter-input]");

            hideSuccessFailure();

            if (inputValue) {
                if ($.inArray(inputValue, previousInputs) > -1) {
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
        },

        logInput = function(input) {
            previousInputs.push(input);
        },

        reload = function() {
            window.location.reload(true);
        }
        
        showFailure = function() {
            $("#success").hide();
            $("#failure").show();
        },

        showRest = function() {

            $.ajax({
                url: '/api/v1.0/remaining_tags',
                data: { 'answered': previousInputs },
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
        },

        showResults = function() {
            var elem = "<p class='text-center margin-top-small'><strong>You remembered " + 
                correctAnswers + " out of " + tagCount + " tag names!</strong></p>";
            $(".form-group.icon-add-on").find("p").remove();
            $(".form-group.icon-add-on").append(elem);
        },

        showSuccess = function() {
            $("#failure").hide();
            $("#success").show();
        },

        toggleDefinitionRow = function() {
            $(this).toggleClass("active-cell");
            $(this).next().toggle();
        },

        switchToRetry = function() {
            $('#retry').show();
            $('#show-all').hide();
        },

        updateCorrectAnswersIndicator = function() {
            $("#tags-left").html(115 - correctAnswers);
        }; 

    $("[name=enter-input]").click(checkTagName);
    showAllButton.click(showRest);
    $("form").submit(function() {
        return false;
    });
    input.keyup(keyUpHandler);
    
    $('#valid-tags, #still-to-learn').on("click","tr.tag-name", toggleDefinitionRow);
    $('#retry').click(function() {
        reload();
    });
});