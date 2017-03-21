//Script to Activate the Carousel
$('.carousel').carousel({
	interval: 5000 //changes the speed
})

$(function() {
    // this is on click event just to demo.
    // You would probably run this at page load or quantity change.
    $("#generate_forms_ingredients").click(function() {
		// update total form count
		quantity = $("[name=quantity]").val();
		$("[name=form-TOTAL_FORMS]").val(quantity);  

		// copy the template and replace prefixes with the correct index
		for (i=0;i<quantity;i++) {
			// Note: Must use global replace here
			html = $("#form_template_ingredients").clone().html().replace(/__prefix_/g, i);
			$("#forms_ingredients").append(html);
		};
		})
	})
	
$(function() {
    // this is on click event just to demo.
    // You would probably run this at page load or quantity change.
    $("#generate_forms_instructions").click(function() {
		// update total form count
		quantity = $("[name=quantity]").val();
		$("[name=form-TOTAL_FORMS]").val(quantity);  

		// copy the template and replace prefixes with the correct index
		for (i=0;i<quantity;i++) {
			// Note: Must use global replace here
			html = $("#form_template_instructions").clone().html().replace(/__prefix_/g, i);
			$("#forms_instructions").append(html);
		};
		})
	})