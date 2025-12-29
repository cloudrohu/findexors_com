(function ($) {
  $(document).ready(function () {

    const cityField = $("#id_city");
    const localityField = $("#id_locality");
    const subLocalityField = $("#id_sub_locality");
    const projectField = $("#id_project");

    // ================= RESET FUNCTIONS =================
    function resetLocality() {
      localityField.html('<option value="">---------</option>');
    }

    function resetSubLocality() {
      subLocalityField.html('<option value="">---------</option>');
    }

    function resetProject() {
      projectField.html('<option value="">---------</option>');
    }

    // ================= CITY → LOCALITY =================
    cityField.on("change", function () {
      const cityId = $(this).val();

      resetLocality();
      resetSubLocality();
      resetProject();

      if (!cityId) return;

      $.ajax({
        url: "/ajax/load-localities/",
        data: { city: cityId },
        success: function (data) {
          localityField.html(data);
        },
        error: function () {
          console.error("❌ Locality AJAX failed");
        }
      });
    });

    // ================= LOCALITY → SUB LOCALITY + PROJECT =================
    localityField.on("change", function () {
      const localityId = $(this).val();

      resetSubLocality();
      resetProject();

      if (!localityId) return;

      // Sub Locality
      $.ajax({
        url: "/ajax/load-sub-localities/",
        data: { locality: localityId },
        success: function (data) {
          subLocalityField.html(data);
        }
      });

      // Project
      $.ajax({
        url: "/ajax/load-projects/",
        data: { locality: localityId },
        success: function (data) {
          projectField.html(data);
        }
      });
    });

    // ================= EDIT MODE AUTO LOAD =================
    if (cityField.val()) {
      cityField.trigger("change");
    }

    if (localityField.val()) {
      localityField.trigger("change");
    }

  });
})(django.jQuery);
