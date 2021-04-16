$(document).ready(function(){

    if ($("#choose-salt-yes").prop("checked")){
        $("#div-salt-input").show();
        }
    else{
        $("#div-salt-input").hide();
    }
    $("#choose-salt").change(function(){
        if ($("#choose-salt-yes").prop("checked")){
           $("#div-salt-input").fadeIn('slow');
           }
        else{
           $("#div-salt-input").fadeOut('slow');
        }
    });

    if (!$("#ecb-dec-op-mode").prop("checked")){
           $("#div-iv-textarea").show();
           }
        else{
           $("#div-iv-textarea").hide();
        }
    $("#div-dec-op-mode").change(function(){
        if (!$("#ecb-dec-op-mode").prop("checked")){
           $("#div-iv-textarea").fadeIn('slow');
           }
        else{
           $("#div-iv-textarea").fadeOut('slow');
        }
    });

    $("#btn-encrypt").click(function(event){
        if ($("#enc-plaintext").val() == "") {
            $("#enc-plaintext").focus();
            alert("Please, type the message to proceed.");
            event.preventDefault();
            return false
        }
    });

    $("#btn-decrypt").click(function(event){
        //var regex_msg = /^([0-9a-f]{16})+$/g
        //var regex_iv = /^[0-9a-f]{16}$/g
        var regex_msg = /^[0-9a-f]+$/g
        var regex_iv = /^[0-9a-f]+$/g
        if (!$("#dec-ciphertext").val().match(regex_msg)){
            $("#dec-ciphertext").focus()
            alert("Ciphertext must contain at least 1 hexadecimal character.")
            event.preventDefault()
            return false
        }
        if($("input[name='dec-op-mode']:checked").val() != "ECB" && !$("#iv-textarea").val().match(regex_iv)){
            $("#iv-textarea").focus()
            alert("IV must contain at least 1 hexadecimal character.")
            event.preventDefault()
            return false
        }
    });

    $("#btn-enc-password").click(function(){
        if($("#enc-password").prop("type") == "password"){
            $("#enc-password").prop("type", "text");
            $("#glyph-eye-enc").text("visibility_off");
        }
        else{
            $("#enc-password").prop("type", "password");
            $("#glyph-eye-enc").text("visibility");
        }
    });

    $("#btn-dec-password").click(function(){
        if($("#dec-password").prop("type") == "password"){
            $("#dec-password").prop("type", "text");
            $("#glyph-eye-dec").text("visibility_off");
        }
        else{
            $("#dec-password").prop("type", "password");
            $("#glyph-eye-dec").text("visibility");
        }
    });
});