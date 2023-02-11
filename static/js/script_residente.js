//añade visitas
function alertarResidente(){
    var serializedData = $("#VisitsForm").serialize();
    console.log(serializedData);
    let opcion = confirm("Está seguro/a que desea crear una visita, a nombre de "+$("#VisitsForm")[0].elements.Nombre.value+" "+$("#VisitsForm")[0].elements.Apellido.value);
    if (opcion == false) return 0;
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
//elimina las visitas
function alertar_delete_residente(number){
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
            alert("error");
        }
    });
    console.log("formulario enviado");
}

//funciones del main residente
function deleteVisitButtonResidente(){
    console.log("redireccionando a eliminar visita");
    window.location.assign(window.location+"deleteVisit")
}

function addVisitButtonResidente(){
    console.log("redireccionando a agregar visita");
    window.location.assign(window.location+"agendVisit")
}