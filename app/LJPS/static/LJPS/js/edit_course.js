// validates that a skill is assigned to the course
$('form').on('submit', function(event) {
    var skill_fulfilled = false
    for (let skill_checkbox of $('.skill')) {
        if (skill_checkbox.checked) {
            skill_fulfilled = true
            break
        }
    }
    if (!skill_fulfilled) {
        event.preventDefault()
        $('#alertModal').modal('show')
        $('#alertMessage').html("Please assign at least one skill to the course!")
        return
    }
})