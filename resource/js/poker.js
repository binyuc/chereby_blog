function poker_check_valid_color() {
    var card_color_flop1 = document.getElementById('card_color_flop1');
    var card_color_flop2 = document.getElementById('card_color_flop2');
    var card_color_flop3 = document.getElementById('card_color_flop3');
    set_progress_rate(0, 100);
    if (card_color_flop1.value == 'none') {
        $("#card_color_flop1").css("border", "red 1px solid");
        return false;
    } else {
        $("#card_color_flop1").css("border", "")
        return true;
    }
    if (card_color_flop2.value == 'none') {
        $("#card_color_flop2").css("border", "red 1px solid");
        return false;
    } else {
        $("#card_color_flop2").css("border", "")
        return true;
    }
    if (card_color_flop3.value == 'none') {
        $("#card_color_flop3").css("border", "red 1px solid");
        return false;
    } else {
        $("#card_color_flop3").css("border", "")
        return true;
    }
}

function set_progress_rate(n, total) {
    //设置进度
    rate = (n / total * 100).toFixed(2)
    if (n >= 0) {
        $(".progress-bar").attr("aria-valuenow", n);
        $(".progress-bar").attr("aria-valuemax", total);
        $(".progress-bar").text(rate + "%");
        $(".progress-bar").css("width", rate + "%");
    }
}

function analyze_card() {
    set_progress_rate(0, 100);
    var canclick = true
    $('#poker_button').attr('disabled', canclick);
    var my_card1 = $.trim($("#card_num_my_hand1").val()) + $.trim($("#card_color_my_hand1").val());
    var my_card2 = $.trim($("#card_num_my_hand2").val()) + $.trim($("#card_color_my_hand2").val());
    var flop1 = $.trim($("#card_num_flop1").val()) + $.trim($("#card_color_flop1").val());
    var flop2 = $.trim($("#card_num_flop2").val()) + $.trim($("#card_color_flop2").val());
    var flop3 = $.trim($("#card_num_flop3").val()) + $.trim($("#card_color_flop3").val());
    var flop4 = $.trim($("#card_num_flop4").val()) + $.trim($("#card_color_flop4").val());
    var flop5 = $.trim($("#card_num_flop5").val()) + $.trim($("#card_color_flop5").val());

    console.log(my_card1, my_card2, flop1, flop2, flop3, flop4, flop5)

    var param = 'my_card1=' + my_card1
        + '&my_card2=' + my_card2
        + '&flop1=' + flop1
        + '&flop2=' + flop2
        + '&flop3=' + flop3
        + '&flop4=' + flop4
        + '&flop5=' + flop5;

    // var ajax = setInterval(function () {
    //     //每1秒请求一次进度
    //     $.ajax({
    //             url: "http://127.0.0.1:5001/progress_bar",
    //             type: "GET",
    //             cache: false,
    //             success: function (response) {
    //                 console.log(response);
    //                 n = response["n"];
    //                 var total = response["total"];
    //                 set_progress_rate(n, total);
    //
    //             }
    //         }
    //     );
    // }, 1000);

    $.post('/poker-run', param, function (data) {

            console.log(data)
            if (data == 'request form get error') {
                alert("解析参数失败")
            } else if (data == 'hand card empty') {
                alert("我的手牌中不能有空值，检查花色和牌面")
            } else if (data == 'flop card empty') {
                alert("转牌区必填3张表，转牌区的牌不可为空，检查花色和牌面")
            } else if (data == 'duplicated card find') {
                alert("有卡牌重复，请检查花色和牌面")
            } else {
                document.getElementById('overall_res').innerText = '我的胜率是 ' + data['my_win_rate'] + '，打平的概率是 ' + data['my_tie_rate'] + '，输掉的概率是 ' + data['my_lose_rate']
                document.getElementById('my_res').innerText = '牌型是【高牌】的概率是 ' + data['my_high_card_prob'] + '，牌型是【一对】的概率是 ' + data['my_pair_prob']
                    + '，牌型是【两对】的概率是 ' + data['my_two_pair_prob'] + '\n' + '牌型是【3条】的概率是 ' + data['my_three_kind_prob'] + '，牌型是【顺子】的概率是 ' + data['my_straight_prob']
                    + '，牌型是【同花】的概率是 ' + data['my_flush_prob'] + '\n' + '牌型是【葫芦】的概率是 ' + data['my_full_house_prob'] + '，牌型是【炸弹】的概率是 ' + data['my_four_kind_prob']
                    + '，牌型是【同花顺】的概率是 ' + data['my_straight_flush_prob'] + '\n' + '牌型是【皇家同花顺】的概率是 ' + data['my_royal_flush_prob']
                document.getElementById('enemy_res').innerText = '牌型是【高牌】的概率是 ' + data['enemy_high_card_prob'] + '，牌型是【一对】的概率是 ' + data['enemy_pair_prob']
                    + '，牌型是【两对】的概率是 ' + data['enemy_two_pair_prob'] + '\n' + '牌型是【3条】的概率是 ' + data['enemy_three_kind_prob'] + '，牌型是【顺子】的概率是 ' + data['enemy_straight_prob']
                    + '，牌型是【同花】的概率是 ' + data['enemy_flush_prob'] + '\n' + '牌型是【葫芦】的概率是 ' + data['enemy_full_house_prob'] + '，牌型是【炸弹】的概率是 ' + data['enemy_four_kind_prob']
                    + '，牌型是【同花顺】的概率是 ' + data['enemy_straight_flush_prob'] + '\n' + '牌型是【皇家同花顺】的概率是 ' + data['enemy_royal_flush_prob']
                document.getElementById('time_diff').innerText = data['time_diff'] + '秒'
            }
            document.getElementById("poker_button").disabled = false;
            set_progress_rate(100, 100);
            // clearInterval(ajax)
        }
    )
}


