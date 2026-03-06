document.addEventListener('DOMContentLoaded', function () {

  console.log('Tracking Games main.js loaded');

  try {
    const dateInput = document.getElementById('id_date');
    if (dateInput && window.MCDatepicker) {
      const picker = MCDatepicker.create({
        el: '#id_date',
        dateFormat: 'yyyy-mm-dd',
        closeOnBlur: true,
        selectedDate: new Date(),
      });

      dateInput.addEventListener('click', () => picker.open());
    } else if (dateInput) {
      console.warn('MCDatepicker not found — date input will remain a plain text input.');
    }
  } catch (err) {
    console.error('Error initializing date picker:', err);
  }
});
