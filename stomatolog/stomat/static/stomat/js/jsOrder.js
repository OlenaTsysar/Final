document.addEventListener("DOMContentLoaded", function () {
    const doctor = document.getElementById("id_doctor");
    const date = document.getElementById("id_date");
    const time = document.getElementById("id_time");

    async function updateTimes() {
        time.innerHTML = "";

        if (!doctor.value || !date.value) {
            time.add(new Option(
                "Сначала выберите врача и дату", ""
            ));
            return;
        }

        time.add(new Option("Загрузка...", ""));

        try {
            const url = new URL(freeTimesUrl, window.location.origin);
            url.searchParams.set("doctor", doctor.value);
            url.searchParams.set("date", date.value);
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error("Не удалось загрузить время");
            }

            const data = await response.json();
            time.innerHTML = "";

            if (data.times.length === 0) {
                time.add(new Option(
                    "Нет свободного времени", ""
                ));
                return;
            }

            time.add(new Option("Выберите время", ""));

            data.times.forEach(function (slot) {
                time.add(new Option(slot, slot));
            });
        } catch (error) {
            time.innerHTML = "";
            time.add(new Option("Ошибка загрузки", ""));
            console.error(error);
        }
    }

    doctor.addEventListener("change", updateTimes);
    date.addEventListener("change", updateTimes);
});