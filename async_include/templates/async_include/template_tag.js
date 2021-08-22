
document.addEventListener("DOMContentLoaded", function(event) {
    const request_frequency = "{{request__frequency}}";

    // Make request function as an unique name
    make_request__{{block_id}} = function (){
        const async_include_url = "{% url 'async_include:get_template' %}";
        const block_id = "{{block_id}}";
        const script_block_id = "script_{{block_id}}";
        const spinner_block_id = "spinner_{{block_id}}";
        const context = {{context|safe}};
        const post_data = {
            path: "{{template_path}}",
            language_code: "{{ language_code }}",
            context: context
        };
        // Delete previous content unless it is the spinner, of course
        try{
            document.querySelector("#{{block_id}} > :not(.async_included-spinner)").remove();
        }catch(TypeError){
        }

        // Show the spinner
        // Note that we try to don't change layout in next requests forcing it to have block's final width
        if(request_frequency != "once"){
            const block_display = document.getElementById(block_id).style.display;
            document.querySelector("#{{block_id}} > .async_included-spinner").style.display = block_display;
        }else{
            document.querySelector("#{{block_id}} > .async_included-spinner").style.display = 'block';
        }
        fetch(async_include_url, {
          method: 'POST',
          body: JSON.stringify(post_data),
          headers:{
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
        	return response.text();
        })
        .then(response_data => {
            if(request_frequency == "once"){
                document.getElementById(block_id).innerHTML = response_data;
                document.getElementById(script_block_id).remove();
            }else{
                document.getElementById(block_id).appendChild(
                    document.createTextNode(response_data)
                );
                const block_width = document.getElementById(block_id).offsetWidth;
                document.querySelector("#{{block_id}} > .async_included-spinner").style.width = block_width;
                document.querySelector("#{{block_id}} > .async_included-spinner").style.display = 'none';
            }
        })
        .catch(response_data => {
            if(request_frequency != "once"){
                clearInterval(make_request_interval_{{block_id}}_id);
            }
        });
    };
    if(request_frequency == "once"){
        make_request__{{block_id}}();
    } else if($.isNumeric(request_frequency) && request_frequency > 0){
        make_request__{{block_id}}();
        make_request_interval_{{block_id}}_id = setInterval(make_request__{{block_id}}, request_frequency*1000);
    }
});
