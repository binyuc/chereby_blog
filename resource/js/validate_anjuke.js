function check_estate() {
    var estate = document.getElementById('estate');
    var pattern = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/;  //用户名格式正则表达式：用户名要至少三位
    if (estate.value.length == 0) {
        $("#estate").val("");
        $("#estate").prop("placeholder", "小区名不可为空");
        $("#estate").css("border", "red 1px solid");
        return false;
    }
    if (pattern.test(estate.value)) {
        $("#estate").val("");
        $("#estate").prop("placeholder", "请勿输入奇怪符号");
        $("#estate").css("border", "red 1px solid");
        return false;
    } else {
        $("#estate").css("border", "")
        return true;
    }
}

function check_area() {
    var area = document.getElementById('area');
    var pattern = /^[0-9]*$/;
    if (area.value.length == 0) {
        $("#area").val("");
        $("#area").prop("placeholder", "面积不可为空");
        $("#area").css("border", "red 1px solid");
        return false;
    }
    if (!pattern.test(area.value)) {
        $("#area").val("");
        $("#area").prop("placeholder", "请输入数字");
        $("#area").css("border", "red 1px solid");
        return false;
    } else {
        $("#area").css("border", "")
        return true;
    }
}

function check_floor() {
    var floor = document.getElementById('floor');
    if (floor.value == 'none') {
        $("#floor").css("border", "red 1px solid");
        return false;
    } else {
        $("#floor").css("border", "")
        return true;
    }
}

function check_bedroom() {
    var bedroom = document.getElementById('bedroom');
    if (bedroom.value == 'none') {
        $("#bedroom").css("border", "red 1px solid");
        return false;
    } else {
        $("#bedroom").css("border", "")
        return true;
    }
}

function check_livingroom() {
    var living_room = document.getElementById('living_room');
    if (living_room.value == 'none') {
        $("#living_room").css("border", "red 1px solid");
        return false;
    } else {
        $("#living_room").css("border", "")
        return true;
    }
}

function check_bathroom() {
    var bathroom = document.getElementById('bathroom');
    if (bathroom.value == 'none') {
        $("#bathroom").css("border", "red 1px solid");
        return false;
    } else {
        $("#bathroom").css("border", "")
        return true;
    }
}

function check_direction() {
    var direction = document.getElementById('direction');
    if (direction.value == 'none') {
        $("#direction").css("border", "red 1px solid");
        return false;
    } else {
        $("#direction").css("border", "")
        return true;
    }
}

function update_neighborhood() {
    var district = document.getElementById('district');
    var param = 'district=' + district.value
    $.post('/anjuke', param, function (data) {
            var listHtml = ''
            data.forEach(function (i) {
                listHtml += `<option>${i}</option>`
            })
            $('#neighborhood').html(listHtml)

        }
    );
}


function check_district() {
    var district = document.getElementById('district');

    if (district.value == 'none') {
        $("#district").css("border", "red 1px solid");
        return false;
    } else {
        $("#district").css("border", "")
        return true;
    }

}

function check_neighborhood() {
    var neighborhood = document.getElementById('neighborhood');
    if (neighborhood.value == 'none') {
        $("#neighborhood").css("border", "red 1px solid");
        return false;
    } else {
        $("#neighborhood").css("border", "")
        return true;
    }
}

function check_built_year() {
    var built_year = document.getElementById('built_year');
    var pattern = /^[0-9]*$/;
    if (built_year.value.length == 0) {
        $("#built_year").val("");
        $("#built_year").prop("placeholder", "建造年限不可为空");
        $("#built_year").css("border", "red 1px solid");
        return false;
    }
    if (!pattern.test(built_year.value)) {
        $("#built_year").val("");
        $("#built_year").prop("placeholder", "请输入数字");
        $("#built_year").css("border", "red 1px solid");
        return false;
    } else {
        $("#built_year").css("border", "")
        return true;
    }
}

function post_model() {
    var estate = $.trim($("#estate").val());
    var area = $.trim($("#area").val());
    var floor = $.trim($("#floor").val());
    var bedroom = ($("#bedroom").val());
    var living_room = ($("#living_room").val());
    var bathroom = ($("#bathroom").val());
    var direction = ($("#direction").val());
    var district = ($("#district").val());
    var neighborhood = ($("#neighborhood").val());
    var built_year = $.trim($("#built_year").val());
    document.getElementById('res_estate').innerText = estate;
    document.getElementById('res_area').innerText = area;
    document.getElementById('res_floor').innerText = floor;
    document.getElementById('res_room').innerText = bedroom + '室' + living_room + '厅' + bathroom + '卫';
    document.getElementById('res_direction').innerText = direction;
    document.getElementById('res_place').innerText = district + '-' + neighborhood;
    document.getElementById('res_built_year').innerText = built_year;

    var param = 'estate=' + estate
        + '&area=' + area
        + '&floor=' + floor
        + '&bedroom=' + bedroom
        + '&living_room=' + living_room
        + '&bathroom=' + bathroom
        + '&direction=' + direction
        + '&district=' + district
        + '&neighborhood=' + neighborhood
        + '&built_year=' + built_year;
    console.log(param)
    $.post('/anjuke-predict', param, function (data) {
            console.log(data)
            if (data == 'model excute failed') {
                alert("模型运行失败，运行错误")

            } else if (data == 'parse parma failed unknown') {
                alert("模型运行失败，入参错误")
            } else {
                document.getElementById('res_model').innerText = '￥' + data;
            }
        }
    )
}