var app = angular.module('workApp', []);
var isLoaded = false
var status_code = 0
var host = 'https://www.freela.co.mz'
//var host = 'http://localhost:8000'

app.controller('loginCtrl', function($scope, $http) {
    var url = host + '/login_register/';
    $scope.projects = []
    $scope.login = function(){
        $http.get(url + '?email=' + $scope.email + '&password='+$scope.password)
        .then(function(res){
            if(res.data.message.includes("Successfully")) location.href = host + '/freelancer-dashboard/';
            else toastMessage(res.data.message, '#Login', res.data.severity)
        });
    }
    $scope.register = function(){
        var data = {
            profile: $scope.profile,
            name: $scope.name,
            email: $scope.email,
            cell: $scope.cell,
            password: $scope.password
        }

        $http({
            url: url,
            method: "POST",
            data: data,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
            }
        }).then(function(res){
            location.href = host + '/freelancer-dashboard/';
        });
    }
    $scope.proposal = function(){
        var data = {
            project: $('#project_id').val(),
            budget: $scope.budget,
            deadline: $scope.deadline,
            description: $scope.description
        }

        $http({
            url: host + '/proposal/',
            method: "POST",
            data: data,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
            }
        }).then(function(res){
            toastMessage(res.data.message, '#Proposta', res.data.severity)
            $("#proposal").modal('hide');
            setTimeout(function(){
                location.reload()
            }, 2000)
        });
    }
    $scope.hire = function(){
        var data = {
            freelancer: sessionStorage.getItem('freela_id'),
            category: $('#category').val(),
            budget: $('#budget').val(),
            description: $('#description').val(),
            exclusive: $('#exclusive').val() == 'on' ? 1 : 0,
            title: $('#title').val()
        }
        $http({
            url: host + '/api/v1/project_invite/',
            method: "POST",
            data: data,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
            }
        }).then(function(res){
            toastMessage(res.data.message, '#Contratar', res.data.severity)
            $("#hire").modal('hide');
        });
	}
    $scope.reset_password = function(){
        $http.get(host + '/reset_password/' + '?email=' + $scope.email)
        .then(function(res){
            toastMessage(res.data.message, '#Senha', res.data.severity)
            if(!res.data.error)
                location.href = host + '/accounts/change_password/?token='+res.data.token;
        });
    }
});

app.controller('freelancerCtrl', function($scope, $http) {
	var url = host + '/api/v1/';

	$scope.save_profile = function(){

	    var data = {
            name: $("#name").val(),
            job_title: $("#job_title").val(),
            speciality: $(".speciality").val(),
            salary: $("#salary").val().replace(',', ''),
            overview: $("#overview").val(),
            city: $("#city").val(),
            address: $("#address").val(),
            mobile: $("#mobile").val()
        }

        $http({
            url: url+'save_profile/',
            method: "POST",
            data: data,
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
            }
        }).then(function(res){
            toastMessage(res.data.message, '#Freelancer', res.data.severity);
        });
	}

    $scope.edit_literary = function(id){
        $http.get(url + 'add_literary/?id=' + id)
        .then(function(res){
            $('#form_literary').modal('show');
            var data = res.data[0].fields;
            $('#id').val(id);
            $('#qualif').val(data.qualification);
            $('#month').val(data.month);
            $('#year').val(data.year);
            $('#institute').val(data.institute);
        });
    }

    $scope.remove_literary = function(id){
        swal({
			  title: 'Eliminar Habilidade!',
              text: "Tem certeza que deseja eliminar esta habilidade?",
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sim!',
              cancelButtonText: 'Cancelar',
		    }).then((result) => {
				if (result.value) {
				    $http({
                        url: url+'add_literary/?id='+id,
                        method: "delete",
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
                        }
                    }).then(function(res){
                        $('.literary_'+id).hide(100);
                        toastMessage('Habilidade removida com sucesso!', '#Habilidades', 'success');
                    });
				}
		    });
    }

    $scope.remove_payment = function(id){
        swal({
			  title: 'Eliminar Forma de Recebimento!',
              text: "Tem certeza que deseja eliminar esta Forma de Recebimento?",
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sim!',
              cancelButtonText: 'Cancelar',
		    }).then((result) => {
				if (result.value) {
				    $http({
                        url: url+'feela_payments/?id='+id,
                        method: "delete",
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
                        }
                    }).then(function(res){
                        toastMessage('Forma de Recebimento removida com sucesso!', '#FormaDeRecebimento', 'success');
                        setTimeout(function(){
                            location.reload()
                        }, 2000);

                    });
				}
		    });
    }

    $scope.edit_payment = function(id){
        $http.get(url + 'feela_payments/?id=' + id)
        .then(function(res){
            $('#form_payments').modal('show');
            var data = res.data[0].fields;
            $('#id').val(id);
            $('#method').val(data.payment_method);
            $('#reference').val(data.account);
        });
    }

    $scope.add_technical_skill = function(){
        console.log($('.select_skills').val())

        $http({
                url: url+'technical_skill/',
                method: "POST",
                data: { 'skills': $('.select_skills').val() },
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
                }
            }).then(function(res){
                toastMessage(res.data.message, '#Skills', res.data.severity);
            });
    }

    $scope.change_password = function(){
        $http.get(url + 'change_password/?old_password=' + $scope.old_password + '&new_password='+$scope.new_password)
        .then(function(res){

            if(res.data.error != 'False'){
                location.href = '/login/';
            }else
                toastMessage(res.message, '#Password', "error");
        });
    }
    $scope.selectPlan = function(){
        $('.pay-btn').text('MZN'+$scope.plan+' Pagar');
        $('#amount').val($scope.plan);
    }
});

function toastMessage(msg, title, severity){
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-center",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1500",
        "timeOut": "10000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
    toastr[severity](msg, title)
}

function reset_password(){
    $.ajax({
        type: 'get',
        url: host + '/reset_password/' + '?email=' + $('#email').val(),
        success: function(res){
            toastMessage(res.message, '#Reset', 'info');
            $('#email').val("");
            $("#reset").modal('hide');
        },
        error: function(res){
            toastMessage(res.message, '#Reset', 'info');
        }
    });
}

$('#form_bug_report').on("submit",function(){
    var data = {
        title: $('#bug_title').val(),
        url: $('#bug_url').val(),
        description: $('#bug_description').val(),
        type: $('#bug_type').val()
	}

    $.ajax({
        type: "POST",
        url: host + '/api/v1/bug_report/',
        data: JSON.stringify(data),
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
             'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
        },
        success: function(data)
        {
            if(data.error == 1 || data.error == "1")
                toastMessage(data.message, "#Feedback", 'error');
            else{
                toastMessage(data.message, "#Feedback", 'success');
                $("#bug").modal('hide');
                $('#form_bug_report').reset();
            }
        },error: function(err)
        {
            console.log(err)
        }
    });
    return false;
});

$('.dashboard-verticle-nav .nav-link').on("click",function(){
      var $target = $('html,body');
      $target.animate({scrollTop: 0}, 600);
});

$('.scroll').click(function(){
    var $target = $('html,body');
    $target.animate({scrollTop: 0}, 600);
})

$('.rating').click(function(){
    var from = $(this).data('from'),
        to =  $(this).data('to');

    if(from == 'None' || to == 'None'){
        alert('invalid');
        return false;
    }

    $("#rate").modal('show');
    $('#freela').val(to);
});

$('.dashboard-verticle-nav li').on("click",function(){
    $('.dashboard-verticle-nav li').removeClass('actived');
    $('.tab-pane').removeClass('active');
    $($(this).find('a').attr('href')).addClass('active');
    $(this).addClass('actived');
});

$( '.friend-drawer--onhover' ).on( 'click',  function() {
  $( '.chat-bubble' ).hide('slow').show('slow');
});

$('#btn-save-payment').on('click', function(){
    var metodo = "put";
    var url = host + '/api/v1/feela_payments/'

    var dados = {
            id: $('#id').val(),
            method: $('#method').val(),
            reference: $('#reference').val()
	}

	if(dados.id == null || dados.id == '') metodo = "post";

	if(dados.reference == '' || dados.reference.length < 6){
        toastMessage('Por favor digite uma referência válida.', "#FormaDeRecebimento", "error");
        return false;
	}

	$.ajax({
        type: metodo,
        url: url,
        data: JSON.stringify(dados),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
             'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
        },
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        success: function(res){
            if (!res.error == 'True' || !res.error == true){
                $("#form_payments").modal('hide');
                toastMessage(res.message, "#FormaDeRecebimento", "success");
                setTimeout(function(){
                    location.reload()
                }, 2000);
            }else{
                toastMessage(res.message, "#FormaDeRecebimento", "warning");
            }
        },
        error: function(res){
            toastMessage("Ocorreu um erro ao processar, por favor tente novamente!", "#FormaDeRecebimento", "error")
        }
    });
});

$('#btn-save-literary').on('click', function(){
    var metodo = "put";
    var url = host + '/api/v1/add_literary/'

    var data = {
            id: $('#id').val(),
            qualification: $('#qualif').val(),
            month: formatDate($('#month').val()),
            year: formatDate($('#year').val()),
            institute: $('#institute').val()
	}

	if(data.id == null || data.id == '') metodo = "post";

	$.ajax({
        type: metodo,
        url: url,
        data: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
             'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
        },
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        success: function(res){
            $("#form_literary").modal('hide');
            toastMessage(res.message, "#Habilidades", "success");

            setTimeout(function(){
                location.reload()
            }, 2000);
        },
        error: function(res){
            toastMessage("Ocorreu um erro ao processar o seu pedido!", "#M-Pesa", "error")
        }
    });
});

$('.btn-action-proposal').click(function(){
    var id = $(this).data('id'), act = $(this).data('action')
    var action = $(this).attr('title')

    swal({
			  title: action + ' Proposta!',
              text: "Tem certeza que deseja "+ action +" esta Proposta?",
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sim!',
              cancelButtonText: 'Cancelar',
		    }).then((result) => {
				if (result.value) {
				$.ajax({
                        type: 'get',
                        url: host + '/proposal/?id='+id +'&action='+ act,
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8'
                        },
                        success: function(res){
                            if (!res.error == 'True' || !res.error == true){
                                toastMessage(res.message, "#Proposta", "success");
                                setTimeout(function(){
                                   location.reload()
                                }, 2000);
                            }else{
                                toastMessage(res.message, "#Proposta", "warning");
                            }
                        },
                        error: function(res){
                            toastMessage("Ocorreu um erro ao processar, por favor tente novamente!", "#FormaDeRecebimento", "error")
                        }
                    });
				}
		    });
});

$('.btn-action-project').click(function(){
    var id = $(this).data('id'), act = $(this).data('action');
    var title = act == 'pd' ? 'Pagamento Efectuado!' : 'Cancelar Projecto!'
    var msg = act == 'pd' ? 'Tem certeza que o Pagamento foi Efectuado?' : "Tem certeza que deseja cancelar este Projecto?"

     swal({
			  title: title,
              text: msg,
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sim!',
              cancelButtonText: 'Cancelar',
		    }).then((result) => {
				if (result.value) {
				$.ajax({
                        type: 'get',
                        url: host + '/project/?id='+id +'&action='+ act,
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8'
                        },
                        success: function(res){
                            if (!res.error == 'True' || !res.error == true){
                                toastMessage(res.message, "#Projecto", "success");
                                setTimeout(function(){
                                   location.reload()
                                }, 2000);
                            }else{
                                toastMessage(res.message, "#Projecto", "warning");
                            }
                        },
                        error: function(res){
                            toastMessage("Ocorreu um erro ao processar, por favor tente novamente!", "#FormaDeRecebimento", "error")
                        }
                    });
				}
		    });
});


$('.btn-action-hire').click(function(){
    var id = $(this).data('id'), act = $(this).data('action');
    var action = $(this).attr('title')

    if (action == 'Aceitar'){
        swal({
          title: 'Quanto você quer receber no Projecto ?',
          input: 'text',
          inputAttributes: {
            autocapitalize: 'off'
          },
          showCancelButton: true,
          confirmButtonText: 'Enviar',
          showLoaderOnConfirm: true,
          cancelButtonText: 'Cancelar',
          cancelButtonColor: '#d33',
          preConfirm: (login) => {
            return fetch(`//api.github.com/users/${login}`)
              .then(response => {
                if (!response.ok) {
                  throw new Error(response.statusText)
                }
                return response.json()
              })
              .catch(error => {

              })
          }
        }).then((result) => {
             $.ajax({
                 type: 'get',
                 url: host + '/api/v1/project_invite/?id='+id +'&action='+ act + '&v='+result.value.login,
                 headers: {
                     'Content-Type': 'application/json; charset=UTF-8'
                 },
                 success: function(res){
                     if (!res.error == 'True' || !res.error == true){
                         toastMessage(res.message, "#Proposta", "success");
                         setTimeout(function(){
                            location.reload()
                         }, 2000);
                     }else{
                        toastMessage(res.message, "#Proposta", res.severity);
                     }
                 },
                 error: function(res){
                    toastMessage("Ocorreu um erro ao processar, por favor tente novamente!", "#FormaDeRecebimento", "error")
                 }
             });
        })
    }else{

         swal({
                  title: action + ' Convite!',
                  text: "Tem certeza que deseja "+ action +" este Convite?",
                  icon: 'warning',
                  showCancelButton: true,
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  confirmButtonText: 'Sim!',
                  cancelButtonText: 'Cancelar',
                }).then((result) => {
                    if (result.value) {
                    $.ajax({
                            type: 'get',
                            url: host + '/api/v1/project_invite/?id='+id +'&action='+ act,
                            headers: {
                                'Content-Type': 'application/json; charset=UTF-8'
                            },
                            success: function(res){
                                if (!res.error == 'True' || !res.error == true){
                                    toastMessage(res.message, "#Convite", "success");
                                    setTimeout(function(){
                                       location.reload()
                                    }, 2000);
                                }else{
                                    toastMessage(res.message, "#Convite", "warning");
                                }
                            },
                            error: function(res){
                                toastMessage("Ocorreu um erro ao processar, por favor tente novamente!", "#FormaDeRecebimento", "error")
                            }
                        });
                    }
                });
    }
});

$('#btn-hire-confirm').click(function(){
    if(location.href.includes("invite")){
        $.ajax({
		type: 'get',
		url: host + '/api/v1/invite/confirm/' + $(this).data('id') +'/',
		success: function(res){
			swal({type: 'success', title: 'A Contratação foi confirmada, sucessos no projecto!'});
			setTimeout(function(){
				location.href = '/employer-dashboard/'
			}, 3500);
		},
		error: function(res){
			toastMessage("Ocorreu um erro ao confirmar a Contratação!", "#Contratação", "error")
		}
	});
    }else{
        $.ajax({
		type: 'get',
		url: host + '/api/v1/proposal/confirm/' + $(this).data('id') +'/',
		success: function(res){
			swal({type: 'success', title: 'A Proposta foi confirmada, sucessos no projecto!'});
			setTimeout(function(){
				location.href = '/employer-dashboard/'
			}, 3500);
		},
		error: function(res){
			toastMessage("Ocorreu um erro ao confirmar a Proposta!", "#Proposta", "error")
		}
	});
    }
});

$('#btn-rate').click(function(){
    var rate = $("input[name='rating']").filter(":checked").val();
    var freela = $("#freela").val()
     $.ajax({
        type: 'get',
        url: host + '/api/v1/review/' + '?freela='+ freela + '&rate=' + rate,
        success: function(res){
            $("#rate").modal('hide');

            setTimeout(function(){
                swal({type: 'success', title: 'Classificação foi enviada!'});
            }, 1000);

            setTimeout(function(){
                location.reload()
            }, 2000);
        },
        error: function(res){
            toastMessage("Ocorreu um erro ao enviar a classificação!", "#Review", "error")
        }
    });
});

function formatDate(date){
    if(date.includes('/')){
        data = date.split("/");
        data = data[2]+"-"+data[0]+"-"+data[1];
        return data;
    }
    return date;
}

function sendPayment(){
    var isLoading = true;
    var data = { 'package': $('#package').val(), 'phone':  $('#phone').val() };
    toastMessage("Por favor confirme a transação no seu celular!", "#M-Pesa", "info")

    $('.pay-btn').html('(<span id="timer">60</span>) Por favor confirme a transação...').prop('disabled', true);
    $('.input-field').prop('disabled', true);

    modalPopUp(60000);
    $.ajax({
        type: 'GET',
        url: host + '/api/v1/send_payment/?package='+data.package+'&phone='+data.phone,
        success: function(res){
            isLoaded = true
            status_code = res.status

            if(status_code == 201) {
                location.href = '/checkout/completed/?tk=' + res.token
                $("input[type=text]").val("");
            }else{
                toastMessage(res.message, "#M-Pesa", "error");
                setTimeout(function(){
                    //location.reload()
                }, 4000)
            }
        },
        error: function(res){
            toastMessage("Ocorreu um erro interno, por favor tente novamente!", "#M-Pesa", "error");
            setTimeout(function(){
                //location.reload()
            }, 4000)
        }
    });
    return false;
}

function changeProject(){
	$('#budget').prop('disabled', false);
}

function projectItemSelected(obj){
	$('#label-propose').text('Proposta ('+$(obj).data('min')+' ~ ' + $(obj).data('max')+')');
	$('#budget').val(parseFloat($(obj).data('max'))/2);
}

// Show the modal window in last 2 minutes
function modalPopUp(time) {
      var remainingTime = time - 60000; // time is in miliseconds
      var timeCount = document.getElementById('timer');
      var loader = 0
      setTimeout(function() { // show the modal and display the remaining time to the user
        var refreshId = setInterval(function(){
          time = time - 1000; //reduce each second
          timeCount.innerHTML = (time/1000)%60;
          if(loader == 60 || isLoaded && status_code != 201){
            clearInterval(refreshId);
            $('.pay-btn').text('Tentar novamente !').prop('disabled', true);
            setTimeout(function(){
                //location.reload()
            }, 4000)
          }
          loader = loader + 1
        }, 1000);
      }, remainingTime);
    }

$(function() {
    "use strict";
    $('#proposal').on('show.bs.modal', function (event) {
        if($('.act-buttons').length == 1) location.href = '/login'
        $('#modal-title').text($(event.relatedTarget).data('title'));
        $('#project_id').val($(event.relatedTarget).data('code'));
    });
    $('#hire').on('show.bs.modal', function (event) {
        if($('.act-buttons').length == 1) location.href = '/login';
		$('#freelancer_name').text($(event.relatedTarget).data('freelancer'));
		sessionStorage.setItem('freela_id', $(event.relatedTarget).data('freela-id'));
    });
    $('.modal').on('hidden.bs.modal', function () {
       $(this).find("input, textarea").val("");
       $(this).find("select").val("1");
       $('#id').val("")
    });
	// Loader
	$(window).on('load', function () {
		$('.Loader').delay(350).fadeOut('slow');
		$('body').delay(350).css({ 'overflow': 'visible' });
	})
    var o = function() {
        var o = 390,
            n = (window.innerHeight > 0 ? window.innerHeight : this.screen.height) - 1;
        n -= o, 1 > n && (n = 1), n > o && $(".page-wrapper").css("min-height", n + "px")
    };
    $(window).on('ready', o), $(window).on("resize", o), $(function() {
        $('[data-toggle="tooltip"]').tooltip()
    }), $(function() {
        $('[data-toggle="popover"]').popover()
    }), jQuery(document).on("click", ".nav-dropdown", function(o) {
        o.stopPropagation()
    }), jQuery(document).on("click", ".navbar-nav > .dropdown", function(o) {
        o.stopPropagation()
    }), $(".dropdown-submenu").on('click', function() {
        $(".dropdown-submenu > .dropdown-menu").toggleClass("show")
    }), $("body").trigger("resize");

    var n = $(window);

    n.on("load", function() {
        var o = n.scrollTop(),
            e = $(".topbar");
        o > 500 ? e.addClass("fixed-header") : e.removeClass("fixed-header")

        if (o > 600){
            $('.header .alert').hide()
        }else{
            $('.header .alert').show()
        }
    }), $(window).on('scroll', function() {
        $(window).scrollTop() >= 600 ? ($(".topbar").addClass("fixed-header"), $(".bt-top").addClass("visible")) : ($(".topbar").removeClass("fixed-header"), $(".bt-top").removeClass("visible"))

        if ($(window).scrollTop() >= 600){
            $('.header .alert').hide()
        }else{
            $('.header .alert').show()
        }
    }), AOS.init(), $(".bt-top").on("click", function(o) {
        o.preventDefault(), $("html,body").animate({
            scrollTop: 0
        }, 600)
    })
	// Jobs
	$("#job-slide").owlCarousel({
		loop:true,
		autoplay:true,
		nav:false,
		dots:false,
		margin:0,
		responsiveClass:true,
		responsive:{
			0:{
				items:1,
				nav:false
			},
			600:{
				items:2,
				nav:false
			},
			1000:{
				items:3,
				nav:false,
				loop:false
			}
		}
	})
	
	// Jobs
	$("#testimonial-3-slide").owlCarousel({
		loop:true,
		autoplay:true,
		nav:false,
		dots:true,
		margin:0,
		responsiveClass:true,
		responsive:{
			0:{
				items:1,
				nav:false
			},
			600:{
				items:1,
				nav:false
			},
			1000:{
				items:1,
				nav:false,
				loop:false
			}
		}
	})
	
	// Jobs
	$("#agency-slide").owlCarousel({
		loop:true,
		autoplay:true,
		nav:false,
		dots:true,
		margin:0,
		responsiveClass:true,
		responsive:{
			0:{
				items:1,
				nav:false
			},
			600:{
				items:2,
				nav:false
			},
			1000:{
				items:3,
				nav:false,
				loop:false
			}
		}
	})
	
	// RL List
	$("#rl-list").owlCarousel({
		loop:true,
		autoplay:true,
		nav:false,
		dots:true,
		margin:0,
		responsiveClass:true,
		responsive:{
			0:{
				items:1,
				nav:false
			},
			600:{
				items:1,
				nav:false
			},
			1000:{
				items:2,
				nav:false,
				loop:false
			}
		}
	})
	
	// Testimonials 2
	$("#testimonials-two").owlCarousel({
		nav:true,
		dots:false,
		items: 1,
		center:false,
		loop: !0,
		navText: ['<i class="fa fa-arrow-left"></i>', '<i class="fa fa-arrow-right"></i>'],
		responsive: {
			0: {items:1,
				stagePadding: 0,
				margin: 0
			},
			768: {items:2,
				stagePadding:0,
				margin:10
			},
			1025: {items:3,
				stagePadding:0,
				margin:10
			},
			1700: {items:3,
				stagePadding:0,
				margin:10
			}
		}
	})

	// All Select Category
	$('.category').select2({
		placeholder: "Choose Category...",
		allowClear: true
	});

	// All Select Category
	$('#category-2').select2({
		placeholder: "Choose Category...",
		allowClear: true
	});
	
	// Filter Sidebar Category
	$('#category-3').select2({
		placeholder: "Choose Category...",
		allowClear: true
	});
	
	// All Search
	$('.speciality').select2({
		placeholder: "Escolher Especialidade...",
		allowClear: true
	});
	
	// Job type
	$('.city').select2({
		placeholder: "Escolher Cidade...",
		allowClear: true
	});
	
	// Career  Lavel
	$('#career-lavel').select2({
		placeholder: "Nível de Experiência...",
		allowClear: true
	});
	
	// Offerd Salary
	$('#offerd-sallery').select2({
		placeholder: "Escolher Orçamento...",
		allowClear: true
	});
	
	// Experience
	$('#experience').select2({
		placeholder: "Escolher Prazo...",
		allowClear: true
	});
	
	// Gender
	$('#gender').select2({
		placeholder: "Please Select",
		allowClear: true
	});	
	
	// Industry
	$('#industry').select2({
		placeholder: "Please Select",
		allowClear: true
	});
	
	// Business Type
	$('#business-type').select2({
		placeholder: "Search Allow",
		allowClear: true
	});
	
	// Search Page Tag & Skill 
	$(".tag-skill").select2({
	  tags: true
	});
	
	// Specialisms 
	$("#specialisms").select2({
		placeholder: "Escolher Habilidades..."
	});

	// Editor 
	$('#summernote').summernote({
		height: 150
	});
	
	// Editor 
	$('#resume-info').summernote({
		height: 120
	});
	
	// Job Description
	$('#jb-description').summernote({
		height: 150
	});
	
	// CV 
	$('#cv-cover').summernote({
		height: 150
	});
	
	// File upload
	$(".custom-file-input").on("change", function() {
	  var fileName = $(this).val().split("\\").pop();
	  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
	});
	
	/****----- Counter ---------*/
	$('.count').on('each', function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 4000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});

	$('.datepicker').datepicker({dateFormat: 'yy-mm-dd'});
});