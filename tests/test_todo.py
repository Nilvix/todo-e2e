def test_page_opens(app, driver):
    assert driver.title == "To-Do List"
    assert app.items() == []
    assert app.counter() == "Осталось задач: 0"


def test_add_task(app):
    app.add("Купить молоко")
    assert app.texts() == ["Купить молоко"]
    assert app.counter() == "Осталось задач: 1"


def test_add_several_tasks_keeps_order(app):
    for t in ["Первая", "Вторая", "Третья"]:
        app.add(t)
    assert app.texts() == ["Первая", "Вторая", "Третья"]


def test_empty_task_shows_error(app):
    app.add("   ")
    assert app.items() == []
    assert app.error() == "Введите текст задачи"


def test_error_hides_after_valid_task(app):
    app.add("")
    app.add("Нормальная задача")
    assert app.error() == ""


def test_complete_task(app):
    app.add("Сделать отчёт")
    app.add("Сдать отчёт")
    app.toggle("Сделать отчёт")
    assert "done" in app.item("Сделать отчёт").get_attribute("class")
    assert app.counter() == "Осталось задач: 1"


def test_delete_task(app):
    app.add("Удалить меня")
    app.add("Оставить")
    app.delete("Удалить меня")
    assert app.texts() == ["Оставить"]


def test_filters(app):
    app.add("Активная")
    app.add("Готовая")
    app.toggle("Готовая")
    app.filter("active")
    assert app.texts() == ["Активная"]
    app.filter("done")
    assert app.texts() == ["Готовая"]
    app.filter("all")
    assert app.texts() == ["Активная", "Готовая"]


def test_clear_done(app, driver):
    app.add("Раз")
    app.add("Два")
    app.toggle("Раз")
    driver.find_element(*app.CLEAR_DONE).click()
    assert app.texts() == ["Два"]


def test_tasks_survive_reload(app, driver):
    app.add("Не потеряться")
    driver.refresh()
    assert app.texts() == ["Не потеряться"]


def test_html_is_not_executed(app):
    app.add("<b>жирный</b>")
    assert app.texts() == ["<b>жирный</b>"]
