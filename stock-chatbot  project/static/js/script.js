$(document).ready(function() {
    
    scrollToBottom();
    
    
    $("#send-btn").click(sendMessage);
    
    
    $("#user-input").keypress(function(e) {
        if (e.which === 13) {
            sendMessage();
        }
    });
    
    
    $(".quick-action-btn").click(function() {
        const query = $(this).data("query");
        $("#user-input").val(query);
        sendMessage();
    });
    
    
    const micBtn = $("#mic-btn");
    let recognition;
    
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        micBtn.click(function() {
            if ($(this).hasClass("listening")) {
                recognition.stop();
                $(this).removeClass("listening");
            } else {
                recognition.start();
                $(this).addClass("listening");
            }
        });
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            $("#user-input").val(transcript);
            micBtn.removeClass("listening");
            sendMessage();
        };
        
        recognition.onerror = function(event) {
            micBtn.removeClass("listening");
            appendMessage("bot", "Sorry, I couldn't understand your voice. Please try typing instead.");
        };
    } else {
        micBtn.hide();
    }
    
    function sendMessage() {
        const userInput = $("#user-input").val().trim();
        
        if (userInput === "") return;
        
        appendMessage("user", userInput);
        $("#user-input").val("");
        
        
        showTypingIndicator();
        
        
        setTimeout(() => {
            $.ajax({
                url: "/get_stock",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ stock: userInput }),
                success: function(response) {
                    hideTypingIndicator();
                    
                    if (response.error) {
                        appendMessage("bot", `<span class="error-message">⚠️ ${response.error}</span>`);
                    } else {
                        const stockMessage = createStockCard(response);
                        appendMessage("bot", stockMessage);
                    }
                },
                error: function() {
                    hideTypingIndicator();
                    appendMessage("bot", `<span class="error-message">⚠️ Sorry, I couldn't fetch the stock data. Please try again later.</span>`);
                }
            });
        }, 800);
    }
    
    function appendMessage(sender, message) {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const messageElement = `
            <div class="message ${sender}-message">
                <div class="message-content">
                    <img src="${sender === 'bot' ? '/static/images/bot-icon.png' : ''}" 
                         alt="${sender === 'bot' ? 'Bot' : 'User'}" 
                         class="message-avatar">
                    <div class="message-text">
                        ${message}
                    </div>
                </div>
                <div class="message-time">${timeString}</div>
            </div>
        `;
        
        $("#chat-container").append(messageElement);
        scrollToBottom();
    }
    
    function createStockCard(stockData) {
        const changeClass = stockData.change.startsWith('+') ? 'positive' : 'negative';
        
        return `
            <div class="stock-card">
                <div class="stock-name">${stockData.name} (${stockData.symbol})</div>
                <div>
                    <span class="stock-price">₹${stockData.price}</span>
                    <span class="stock-change ${changeClass}">${stockData.change}</span>
                </div>
                <div class="stock-details">
                    <div class="stock-detail">
                        <span class="stock-detail-label">Day High:</span>
                        <span class="stock-detail-value">₹${stockData.high}</span>
                    </div>
                    <div class="stock-detail">
                        <span class="stock-detail-label">Day Low:</span>
                        <span class="stock-detail-value">₹${stockData.low}</span>
                    </div>
                    <div class="stock-detail">
                        <span class="stock-detail-label">52W High:</span>
                        <span class="stock-detail-value">₹${stockData["52_week_high"]}</span>
                    </div>
                    <div class="stock-detail">
                        <span class="stock-detail-label">52W Low:</span>
                        <span class="stock-detail-value">₹${stockData["52_week_low"]}</span>
                    </div>
                </div>
            </div>
            <p>Here's the latest data for ${stockData.name}. What else would you like to know?</p>
        `;
    }
    
    function scrollToBottom() {
        const container = $("#chat-container");
        container.scrollTop(container[0].scrollHeight);
    }
    
    function showTypingIndicator() {
        $("#typing-indicator").css("display", "flex");
        scrollToBottom();
    }
    
    function hideTypingIndicator() {
        $("#typing-indicator").hide();
    }
    
    
    setTimeout(() => {
        appendMessage("bot", "You can also click the quick buttons above for popular stock queries!");
    }, 1500);
});