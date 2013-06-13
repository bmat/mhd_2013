var map;
$(document).ready(function() {
      // ##### CUSTOMER #####
      // Get id value
      $(".edit_customer").click(function() {
      	// Get row
      	row = $(this).parent().parent()
      	// Get item values
      	iid = row.find(".iid").text()
      	password = row.find(".password").text()
      	email = row.find(".email").text()
        // Copy values into form
        $('.form_customer > input[name="iid"]').val(iid)
        $('.form_customer > input[name="email"]').val(email)
        $('.form_customer > input[name="password"]').val(password)
      });
      // ##### DRIVER #####
      // Get id value
      $(".edit_driver").click(function() {
        // Get row
        row = $(this).parent().parent()
        // Get item values
        iid = row.find(".iid").text()
        first_name = row.find(".first_name").text()
        last_name = row.find(".last_name").text()
        phone1 = row.find(".phone1").text()
        phone2 = row.find(".phone2").text()
        email = row.find(".email").text()
        // Copy values into form
        $('.form_driver > input[name="iid"]').val(iid)
        $('.form_driver > input[name="first_name"]').val(first_name)
        $('.form_driver > input[name="last_name"]').val(last_name)
        $('.form_driver > input[name="phone1"]').val(phone1)
        $('.form_driver > input[name="phone2"]').val(phone2)
        $('.form_driver > input[name="email"]').val(email)
      });
      // ##### VEHICLE #####
      // Get id value
      $(".edit_vehicle").click(function() {
        // Get row
        row = $(this).parent().parent()
        // Get item values
        iid = row.find(".iid").text()
        plate = row.find(".plate").text()
        license = row.find(".license").text()
        model = row.find(".model").text()
        seats = row.find(".seats").text()
        driver_id = row.find(".driver").attr('name')
        // Copy values into form
        $('.form_vehicle > input[name="iid"]').val(iid)
        $('.form_vehicle > input[name="plate"]').val(plate)
        $('.form_vehicle > input[name="license"]').val(license)
        $('.form_vehicle > input[name="model"]').val(model)
        $('.form_vehicle > input[name="seats"]').val(seats)
        $('.form_vehicle > select[name="driver_id"]').val(driver_id)
      });
      // ##### SERVICE #####
      // Get id value
      $(".edit_service").click(function() {
        // Get row
        row = $(this).parent().parent()
        // Get item values
        iid = row.find(".iid").text()
        from_address = row.find(".from").find(".from_address").text()
        start_x = row.find(".from").find(".start_x").text()
        start_y = row.find(".from").find(".start_y").text()
        to_address = row.find(".to").find(".to_address").text()
        end_x = row.find(".to").find(".end_x").text()
        end_y = row.find(".to").find(".end_y").text()
        status = row.find(".status").text()
        customer_id = row.find(".customer_id").attr('name')
        vehicle_id = row.find(".vehicle_id").attr('name')
        // Copy values into form
        $('.form_service > input[name="iid"]').val(iid)
        $('.form_service > input[name="from_address"]').val(from_address)
        $('.form_service > input[name="from_coords"]').val(start_x+','+start_y)
        $('.form_service > input[name="to_address"]').val(to_address)
        $('.form_service > input[name="to_coords"]').val(end_x+','+end_x)
        $('.form_service > input[name="status"]').val(status)
        $('.form_service > select[name="customer_id"]').val(customer_id)
        $('.form_service > select[name="vehicle_id"]').val(vehicle_id)
      });
      // ##### TRACKING #####
      // Create map
      map = new GMaps({
        div: '#tracking_map',
        zoom: 16,
        lat: -12.043333,
        lng: -77.028333,
        click: function(e) {
          $('.form_tracking > input[name="position"]').val(e.latLng.lat()+', '+e.latLng.lng())
        },
        dragend: function(e){
          alert('dragend');
        }
      });

      $('#tracking_map_selector').css("position", "absolute");
      $('#tracking_map_selector').css("left", "-10000px");

      $('.form_tracking > input[name="position"]').focus(function() {
        $('#tracking_map_selector').css("position", "relative");
        $('#tracking_map_selector').css("left", "0px");
      });
      $('.form_tracking > input[name="position"]').blur(function() {
        $('#tracking_map_selector').css("position", "absolute");
        $('#tracking_map_selector').css("left", "-10000px");
      });
});