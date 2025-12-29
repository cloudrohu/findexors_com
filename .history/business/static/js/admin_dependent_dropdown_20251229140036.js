django.jQuery(document).ready(function($) {
    
    var cityField = $('#id_city');
    var localityField = $('#id_locality');
    var subLocalityField = $('#id_sub_locality');
    var projectField = $('#id_project');

    // --- FUNCTION: Dropdown ko Reset aur Disable (Lock) karna ---
    function disableDropdown(field) {
        field.html('<option value="">---------</option>');
        field.prop('disabled', true); // LOCK
        field.css('background-color', '#e9ecef'); // Grey look
        field.css('cursor', 'not-allowed');
    }

    function enableDropdown(field) {
        field.prop('disabled', false); // UNLOCK
        field.css('background-color', '#ffffff'); // White look
        field.css('cursor', 'default');
    }

    // --- INITIAL CHECK (Page Load) ---
    // Agar City khali hai (New Form), to sab lock kar do
    if (!cityField.val()) {
        disableDropdown(localityField);
        disableDropdown(subLocalityField);
        disableDropdown(projectField);
    } 
    // Agar Locality khali hai, to uske neeche wale lock
    else if (!localityField.val()) {
        disableDropdown(subLocalityField);
        disableDropdown(projectField);
    }

    // --- EVENT 1: Jab City Change Hogi ---
    cityField.change(function() {
        var url = "/ajax/load-localities/";  
        var cityId = $(this).val();

        // Niche walo ko pehle lock karo
        disableDropdown(localityField);
        disableDropdown(subLocalityField);
        disableDropdown(projectField);

        if (cityId) {
            $.ajax({
                url: url,
                data: { 'city': cityId },
                success: function(data) {
                    localityField.html(data);
                    enableDropdown(localityField); // Data aane par UNLOCK
                }
            });
        }
    });

    // --- EVENT 2: Jab Locality Change Hogi ---
    localityField.change(function() {
        var url = "/ajax/load-sub-localities/";
        var localityId = $(this).val();

        disableDropdown(subLocalityField);
        disableDropdown(projectField);

        if (localityId) {
            $.ajax({
                url: url,
                data: { 'locality': localityId },
                success: function(data) {
                    subLocalityField.html(data);
                    enableDropdown(subLocalityField); // UNLOCK
                    enableDropdown(projectField); // Project bhi UNLOCK
                }
            });
        }
    });

});