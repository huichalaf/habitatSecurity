function aVisita_admin(){
    console.log("redireccionando a añadir visita");
    window.location.assign(window.location+"agendVisit/")
}
function cVisita_admin(){
    console.log("redireccionando a eliminar visita");
    window.location.assign(window.location+"deleteVisit/")
}
function estacionamiento_admin(){
    console.log("redireccionando a estacionamiento");
    window.location.assign(window.location+"parking/")
}
function agenda_admin(){
    console.log("redireccionando a agenda");
    window.location.assign(window.location+"agenda/")
}
function bitacora_admin(){
    console.log("redireccionando a bitacora");
    window.location.assign(window.location+"bitacora/")
}
function configuracion_admin(){
    console.log("redireccionando a configuracion");
    window.location.assign(window.location+"configuracion/")
}
function qrControl_admin(){
    console.log("redireccionando a ControlVisitas");
    window.location.assign(window.location+"controlVisit/")
}

function alertar_admin(){
    var serializedData = $("#VisitsForm").serialize();
    let opcion = confirm("Está seguro/a que desea crear una visita, a nombre de "+$("#VisitsForm")[0].elements.Nombre.value+" "+$("#VisitsForm")[0].elements.Apellido.value);
    if (opcion == false) return 0;
    console.log(serializedData);
    $.ajax({
        url: $("VisitsForm").data('url'),
        data: serializedData,
        type: 'post',
        success: function(response){
            alert('Añadido exitosamente');
        },
        error: function(data){
            if(data.status==500){
                alert("error interno del servidor");
            }
            if(data.status==417){
                alert("Debes completar todas las casillas obligatorias del formulario");
            }
            if(data.status==412){
                alert("Debes ingresar una fecha válida(no previa al día actual)")
            }
            if(data.status==406){
                alert("Lo siento, no puedes ingresar caracteres especiales en el formulario")
            }
        }
    });
    console.log("formulario enviado");
}

function alertar_delete_admin(number){
    let opcion = confirm("estas seguro que deseas eliminar esta visita? (id "+number+")");
    if (opcion == false) return 0;
    var serializedData = $("#numberForm").serialize();
    console.log(serializedData);
    $.ajax({
        url: $("numberForm").data('url'),
        data: serializedData+'&Number='+number,
        dataType: 'json',
        type: 'post',
        success: function(response){
            alert('Eliminado exitosamente');
        },
        error: function(data){
            alert("error")
        }
    });
    console.log("formulario enviado");
}