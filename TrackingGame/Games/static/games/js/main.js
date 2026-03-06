document.addEventListener('DOMContentLoaded', function () {
  console.log('Tracking Games main.js loaded');

  try {
    // User-provided minimal snippet: create a picker for an element with id 'id_date'
    const dateInput = document.getElementById('id_date');
    if (dateInput && window.MCDatepicker) {
      const picker = MCDatepicker.create({
        el: '#id_date',
        dateFormat: 'yyyy-mm-dd',
        closeOnBlur: true,
        selectedDate: new Date(),
      });
      dateInput.addEventListener('click', () => { try { picker.open(); } catch (e) { console.warn(e); } });
    } else if (dateInput) {
      console.warn('MCDatepicker library not available for #id_date');
    }
  } catch (err) {
    console.error('Error applying user datepicker snippet:', err);
  }
});

// abandon date function because i couldnt get it done 