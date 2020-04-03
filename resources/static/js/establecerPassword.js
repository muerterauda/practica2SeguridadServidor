function establecerPassword() {
    let password_1 = $('#password-1');
    let password_2 = $('#password-2');
    let pass = password_1.val();
    let pass2 = password_2.val();
    if(pass!==pass2){
        $('#alertaNoIguales').show();
        password_1.addClass('is-invalid');
        password_2.addClass('is-invalid');
        password_1.val('');
        password_2.val('');
    }else{
        console.log(2);
    }
    // action="/serviciosBasicos/establecerContraseña" method="POST"
}