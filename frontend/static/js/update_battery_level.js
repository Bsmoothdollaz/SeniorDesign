<script>
  // Define a function to update the battery level
  function updateBatteryLevel() {
    // Make an AJAX request to the /get_battery endpoint in your Flask backend
    fetch('/get_battery')
      .then(response => response.text())
      .then(batteryLevel => {
        // Update the battery level in the navbar
        document.querySelector('#battery-level .battery-level-percent').textContent = batteryLevel + '%';
        document.querySelector('#battery-level .battery-level-fill').style.width = batteryLevel + '%';
      })
      .catch(error => {
        console.error('Error updating battery level:', error);
      });
  }

  // Call the updateBatteryLevel function every 5 seconds
  setInterval(updateBatteryLevel, 5000);
</script>

