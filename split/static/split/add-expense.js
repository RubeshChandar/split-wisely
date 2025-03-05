 document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(checkbox => {
      const amountInput = checkbox.closest('.input-group').querySelector('input[name="split_amount"]');

      function updateAmountInputState() {
        amountInput.disabled = !checkbox.checked;
        if (!checkbox.checked) {
          amountInput.value = ""
        }
      }

      updateAmountInputState(); // Initial state

      checkbox.addEventListener('change', updateAmountInputState);
    });
  });


document.addEventListener('DOMContentLoaded', function() {
    const splitEquallySpan = document.getElementById('split-equally');
    const amountInput = document.getElementById('id_amount');
    const checkboxes = document.querySelectorAll('input[class="form-check-input mt-0"]');
    const amountInputs = document.querySelectorAll('input[name="split_amount"]');

    splitEquallySpan.addEventListener('click', function() {
        const totalAmount = parseFloat(amountInput.value) || 0;
        const checkedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        const checkedCount = checkedCheckboxes.length;
        console.log(checkedCheckboxes)

        if (checkedCount > 0) {
            const share = totalAmount / checkedCount;
            amountInputs.forEach(amountInput => {
                const checkbox = amountInput.closest('.input-group').querySelector('input[type="checkbox"]');
                if (checkbox.checked) {
                    amountInput.value = share.toFixed(2);
                }
            });
        }
    });
});