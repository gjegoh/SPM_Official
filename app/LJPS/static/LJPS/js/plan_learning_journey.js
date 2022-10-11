// ensures that courses that fulfill multiple skills will be checked/unchecked simultaneously
$('form').unbind('change').on('change', ':checkbox', function() {
    if (this.checked) {
        $(`:input[value=${this.value}]`).prop('checked', true)
    }
    else {
        $(`:input[value=${this.value}]`).prop('checked', false)
    }
})

// validates that a course is selected for each required skill
$('form').on('submit', function(event) {
    for (let skill of $('.skill')) {
        var skill_fulfilled = false
        for (let course_checkbox of $(skill).children('.card-body').children('.card').children('ul').children('li:last-child').children(':checkbox')) {
            if (course_checkbox.checked) {
                skill_fulfilled = true
                break
            }
        }
        if (!skill_fulfilled) {
            event.preventDefault()
            $('#alertModal').modal('show')
            $('#alertMessage').html("Please select at least 1 course for each required skill!")
            return
        }
    }
})