
!function($) {
    "use strict";

    var CalendarApp = function() {
        this.$body = $("body")
        this.$calendar = $('#calendar'),
        this.$event = ('#calendar-events div.calendar-events'),
        this.$categoryForm = $('#add_new_event form'),
        this.$extEvents = $('#calendar-events'),
        this.$modal = $('#my_event'),
        this.$saveCategoryBtn = $('.save-category'),
        this.$calendarObj = null,
        this.$modal2 = $('#new_event')
    };


    /* on drop */
    CalendarApp.prototype.onDrop = function (eventObj, date) { 
        var $this = this;
            // retrieve the dropped element's stored Event Object
            var originalEventObject = eventObj.data('eventObject');
            var $categoryClass = eventObj.attr('data-class');
            // we need to copy it, so that multiple events don't have a reference to the same object
            var copiedEventObject = $.extend({}, originalEventObject);
            // assign it the date that was reported
            copiedEventObject.start = date;
            if ($categoryClass)
                copiedEventObject['className'] = [$categoryClass];
            // render the event on the calendar
            $this.$calendar.fullCalendar('renderEvent', copiedEventObject, true);
            // is the "remove after drop" checkbox checked?
            if ($('#drop-remove').is(':checked')) {
                // if so, remove the element from the "Draggable Events" list
                eventObj.remove();
            }
    },
    /* on click on event */
    CalendarApp.prototype.onEventClick =  function (calEvent, jsEvent, view) {


        // $('#add_new_event').modal('show');
        // // $('#add_new_event').find('#title').val(onEventClick.title);
        // $('#add_new_event').find('#prjName').val(calEvent.title);
        // $('#add_new_event').find('#starts-at').val(calEvent.start);
        // $('#add_new_event').find('#ends-at').val(calEvent.end);


        var $this = this;
        var form = $("<form></form>");
        form.append("<label>Edit Work</label>");
        form.append("<div class='input-group'><input class='form-control' type=text value='" + calEvent.title + "' /><span class='input-group-append'><button type='submit' class='btn btn-success'><i class='fa fa-check'></i> Save</button></span></div>");

            // Add Timings  

            // form.append("<label>Change Timing</label>");
            // form.append("<div class='col-xs-6'><label>Select start time:</label><div class='input-group m-b-20'><input class='form-control' type=time /></div>");
            // form.append("<div class='col-xs-6'><label>Select end time:</label><div class='input-group m-b-20'><input class='form-control' type=time /></div>");

            //End Timings

            // form.append("<span class='input-group-append'><button type='submit' class='btn btn-success'><i class='fa fa-check'></i> Save</button></span>");

            $this.$modal.modal({
                backdrop: 'static'
            });
            $this.$modal.find('.delete-event').show().end().find('.save-event').hide().end().find('.modal-body').empty().prepend(form).end().find('.delete-event').unbind('click').click(function () {
                $this.$calendarObj.fullCalendar('removeEvents', function (ev) {
                    return (ev._id == calEvent._id);
                });
                $this.$modal.modal('hide');
            });
            $this.$modal.find('form').on('submit', function () {
                calEvent.title = form.find("input[type=text]").val();
                $this.$calendarObj.fullCalendar('updateEvent', calEvent);
                $this.$modal.modal('hide');
                return false;
            });
    },
    /* on select */
    CalendarApp.prototype.onSelect = function (start, end, allDay) {

        $('#new_event').modal('show');
        //$('#add_new_event').find('#title').val(onSelect.title);
        $('#new_event').find('#starts-at').val(start);
        $('#new_event').find('#ends-at').val(end);


        // var $this = this;
        // $this.$modal.modal({
        //     backdrop: 'static'
        // });
        // var form = $("<form></form>");
        // form.append("<div class='event-inputs'></div>");
        // form.find(".event-inputs")
        //     .append("<div class='form-group'><label class='control-label'>Project Name</label><input class='form-control' placeholder='Insert Project Name' type='text' name='title'/></div>")
        //     .append("<div class='form-group'><label class='control-label'>Description</label><input class='form-control' placeholder='Description' type='text' name='description'/></div>");

            // .append("<div class='form-group'><label class='control-label'>Category</label><select class='form-control' name='category'></select></div>")
            // .find("select[name='category']")
            // .append("<option value='bg-danger'>Danger</option>")
            // .append("<option value='bg-success'>Success</option>")
            // .append("<option value='bg-purple'>Purple</option>")
            // .append("<option value='bg-primary'>Primary</option>")
            // .append("<option value='bg-info'>Info</option>")
            // .append("<option value='bg-warning'>Warning</option></div></div>");

            // Add Timings  

            // form.append("<label>Timing</label>");
            // form.append("<div class='col-xs-6'><label>Select start time:</label><div class='input-group m-b-20'><input class='form-control' type=time /></div>");
            // form.append("<div class='col-xs-6'><label>Select end time:</label><div class='input-group m-b-20'><input class='form-control' type=time /></div>");

            //End Timings

            // $this.$modal.find('.delete-event').hide().end().find('.save-event').show().end().find('.modal-body').empty().prepend(form).end().find('.save-event').unbind('click').click(function () {
            //     form.submit();
            // });

            // My Code
            
            $this.$modal2.find('.modal-body').find(form).end().find('.save-event').unbind('click').click(function () {
                form.submit();
            });

            // $('#add_new_event').find('.submit').click(function(){
            //     form.submit();
            // });

            // $('#add_new_event').find('.submit').on('submit',function(){
            //     var title2 = $('#add_new_event').find("#prjName").val();
            //     var starttime = $('#add_new_event').find("#starts-at").val();
            //     var endtime = $('#add_new_event').find("#ends-at").val();

            //     if (title2 !== null && title2.length != 0) {
            //         $this.$calendarObj.fullCalendar('renderEvent', {
            //             title: title2,
            //             start:starttime,
            //             end: endtime,
            //             allDay: false,
            //             // className: categoryClass
            //         }, true);  
            //         $('#add_new_event').modal('hide');
            //     }
            //     else{
            //         alert('You have to write the project name.');
            //     }
            //     return false;
            // });
            // $this.$calendarObj.fullCalendar('unselect');

            // End Here

            $this.$modal.find('form').on('submit', function () {
                var title = form.find("input[name='title']").val();
                var beginning = form.find("input[name='beginning']").val();
                var ending = form.find("input[name='ending']").val();
                var categoryClass = form.find("input[name='description']").val();
                // var categoryClass = form.find("select[name='category']").val();
                if (title !== null && title.length != 0) {
                    $this.$calendarObj.fullCalendar('renderEvent', {
                        title: title,
                        start:start,
                        end: end,
                        allDay: false,
                        className: categoryClass
                    }, true);  
                    $this.$modal.modal('hide');
                }
                else{
                    alert('You have to write the project name.');
                }
                return false;
                
            });
            $this.$calendarObj.fullCalendar('unselect');
    },
    CalendarApp.prototype.enableDrag = function() {
        //init events
        $(this.$event).each(function () {
            // it doesn't need to have a start or end
            var eventObject = {
                title: $.trim($(this).text()) // use the element's text as the event title
            };
            // store the Event Object in the DOM element so we can get to it later
            $(this).data('eventObject', eventObject);
            // make the event draggable using jQuery UI
            $(this).draggable({
                zIndex: 999,
                revert: true,      // will cause the event to go back to its
                revertDuration: 0  //  original position after the drag
            });
        });
    }
    /* Initializing */
    CalendarApp.prototype.init = function() {
        this.enableDrag();
        /*  Initialize the calendar  */
        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
        var form = '';
        var today = new Date($.now());

        var defaultEvents =  [{
                title: 'Project 4',
                desc: 'Design',
                start: new Date($.now() + 148000000),
                className: 'bg-purple'
            },
            {
                title: 'Project 1',
                desc: 'Back-end',
                start: today,
                end: today,
                className: 'bg-success'
            },
            {
                title: 'Project 2',
                desc: 'SQL',
                start: new Date($.now() + 168000000),
                className: 'bg-info'
            },
            {
                title: 'Project 3',
                desc: 'Design',
                start: new Date($.now() + 338000000),
                className: 'bg-primary'
            }];

        var $this = this;
        $this.$calendarObj = $this.$calendar.fullCalendar({
            slotDuration: '00:15:00', /* If we want to split day time each 15minutes */
            minTime: '00:00:00',
            maxTime: '24:00:00',  
            defaultView: 'agendaWeek',  
            handleWindowResize: true,   
             
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'agendaWeek,month,agendaDay'
            },
            events: defaultEvents,
            editable: true,
            droppable: true, // this allows things to be dropped onto the calendar !!!
            eventLimit: true, // allow "more" link when too many events
            selectable: true,
            drop: function(date) { $this.onDrop($(this), date); },
            select: function (start, end, allDay) { $this.onSelect(start, end, allDay); },
            eventClick: function(calEvent, jsEvent, view) { $this.onEventClick(calEvent, jsEvent, view); }

        });

        //on new event
        this.$saveCategoryBtn.on('click', function(){
            var categoryName = $this.$categoryForm.find("input[name='category-name']").val();
            // var categoryColor = $this.$categoryForm.find("select[name='category-color']").val();
            var categoryColor = $this.$categoryForm.find("input[name='description']").val();
            if (categoryName !== null && categoryName.length != 0) {
                $this.$extEvents.append('<div class="calendar-events" data-class="bg-' + categoryColor + '" style="position: relative;"><i class="fa fa-circle text-' + categoryColor + '"></i>' + categoryName + '</div>')
                $this.enableDrag();
            }

        });
    },

   //init CalendarApp
    $.CalendarApp = new CalendarApp, $.CalendarApp.Constructor = CalendarApp
    
}(window.jQuery),

//initializing CalendarApp
function($) {
    "use strict";
    $.CalendarApp.init()
}(window.jQuery);