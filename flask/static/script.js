$(document).ready(function() {
    // Navbar active item toggle
    $('.navbar-nav .nav-item').click(function() {
        $('.navbar-nav .nav-item').removeClass('active'); // Remove active class from all items
        $(this).addClass('active'); // Add active class to the clicked item
    });

    // Show modal
    window.showModal = function() {
        $('#infoContact').modal('show'); // Show modal using Bootstrap's modal method
    };

    // Close modal on close button click
    $(document).on('click', '.modal .close', function() {
        $(this).closest('.modal').modal('hide'); // Hide modal using Bootstrap's modal method
    });

    // Close modal when clicking outside of it
    $(document).on('click', function(event) {
        if ($(event.target).hasClass('modal')) {
            $(event.target).modal('hide'); // Hide modal using Bootstrap's modal method
        }
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top
        }, 500);
    });

    // Modal toggle function using jQuery
    window.toggleInfo = function(modalId) {
        $('#' + modalId).modal('toggle'); // Toggle visibility of the modal using Bootstrap's modal method
    };

    // Balance check before form submission
    window.checkBalance = function() {
        // Calculate the total cost
        var totalCost = itemPrice * quantity;

        // Check if the balance is sufficient
        if (userBalance >= totalCost) {
            return true; // Allow the form to be submitted
        } else {
            $('#insufficientBalance').text('Insufficient balance.').show(); // Show insufficient balance warning
            return false; // Prevent the form from being submitted
        }
    };
});