$(document).ready(
    
    function() {

            $('#user_tkts').DataTable({
                "pageLength":10,
                "ordering":false,
                "sorting":false,
            });

            var field_id = 0;

            $('#new_input').click(function(e){                            //on add input button click
            e.preventDefault();
            field_id = field_id + 1;

                // to add new input field when creating a new frt. field_id is used to add unique id to each field
                $('#new_input_adder').append(
                    `
                        <div id="each_field" class="input-group mb-3">
                        <input type="text" required class="form-control" placeholder="Enter field name here" name='input${field_id}'>
                        <div class="input-group-append">
                            <span class="input-group-text">
                            <a href='#' class="remove_field"><i class="fa fa-window-close" aria-hidden="true"></i></a>
                            </span>
                        </div>  
                        <select name='field_type${field_id}'>
                        <option value="CharField">Single Line Input</option>
                        <option value="textarea">Multi Line Input</option>
                        <option value="DateField">Date Input</option>
                        <option value="phone_num">Phone Number</option>
                        <option value="number">Number</option>
                        </select>
                        </div>
                    `
                ); 
            });

            //to remove an existing field when creating a new frt
            $("#new_input_adder").on("click",".remove_field", function(e){ 
                e.preventDefault(); 
                $(this).parents('#each_field').remove();
            })

            $(document).on('click','[id^="frt_opener_"]',function(){
                var dept_name = this.getAttribute('data-parent-value1');
                var tkt_name = this.getAttribute('data-parent-value2');
                console.log(tkt_name)
                // console.log(tkt_name)
                // var new_xhr = 
                $.ajax({
                    type: 'Get',
                    url: '/departments/'+dept_name+'/'+tkt_name+'/',
                    success: function(data){
                        // console.log(data.modal_html)
                        $('.modal-title').html(data.heading)
                        $('.modal-body').html(data.modal_html)
                        $('#modal_html').modal('show')
                        
                    }
                })
                //
                
            })

            //to open the modal
            $('#modal_opener').click(function(){
                $('#modal_html').modal('show')
        
            })
            
            $(document).on('click','[id^="reply_for_"]',function(){
                var tkt_id = this.getAttribute('data_parent_value')
                console.log(tkt_id)
                $.ajax({
                    type:'Get',
                    url:'/respond/'+tkt_id+'/',
                    success: function(data){
                        $('.modal-title').html(data.heading)
                        $('.modal-body').html(data.modal_html)
                        $('#modal_html').modal('show')
                    }
                })
              }
            )

            $('#announce').click(function(){
                $.ajax({
                    type: 'Get',
                    url:'/announcements/form',
                    success: function(data){
                        $('.modal-title').html(data.heading)
                        $('.modal-body').html(data.modal_html)
                        $('#modal_html').modal('show')
                    }
                })
            })
});
