const rangeSlider = document.getElementById('range-slider');

if (rangeSlider) {
    noUiSlider.create(rangeSlider, {
        start: [0, 100],
        connect: true,
        step: 5,
        range: {
            'min': [0],
            'max': [100]
        }
    });

    const input0 = document.getElementById('input-0')
    const input1 = document.getElementById('input-1')
    const inputs = [input0, input1]

    rangeSlider.noUiSlider.on('update', function (values, handle) {
        inputs[handle].value = Math.round(values[handle]);
    });

    const setRangeSlider = (i, value) => {
        let num_array = [null, null];
        num_array[i] = value;

        rangeSlider.noUiSlider.set(num_array);
    };

    inputs.forEach((el, index) => {
       el.addEventListener('change', (e) => {
            setRangeSlider(index, e.currentTarget.value);
       });
    });
}