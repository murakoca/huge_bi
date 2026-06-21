from dash import clientside_callback, Output, Input

# JavaScript kodu
clientside_callback(
    """
    function(socketEvent) {
        // socketEvent otomatik olarak gelmez, kendimiz dinleyelim
        var socket = io.connect('/live');
        socket.on('new_sale', function(data) {
            // Gelen veriyi işleyip bir Div içine yaz
            var listElement = document.getElementById('live-list');
            var newItem = document.createElement('li');
            newItem.textContent = data.timestamp + ' - ' + data.product + ': $' + data.sales;
            listElement.prepend(newItem);
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output('live-list', 'children'),
    Input('live-interval', 'n_intervals')  # Sadece tetikleyici, gerçek veri WebSocket'ten
)