function establecerPassword() {
    let password_1 = $('#password-1');
    let password_2 = $('#password-2');
    let pass = password_1.val();
    let pass2 = password_2.val();
    if(pass!==pass2) {
        $('#alertaNoIguales').show();
        password_1.addClass('is-invalid');
        password_2.addClass('is-invalid');
        password_1.val('');
        password_2.val('');
    }else if(pass === ''){
        $('#alertaVacio').show();
        password_1.addClass('is-invalid');
        password_2.addClass('is-invalid');
        password_1.val('');
        password_2.val('');
    }else{
        $.ajax({
            url: '/serviciosBasicos/establecerPassword',
            type: 'POST',
            data: {
                password: pass
            },
            success: function (data) {
                window.location.href = "/";
            },
            error: function (data) {
                alert("Se ha producido un error en el servidor.");
            }
        });
    }
}