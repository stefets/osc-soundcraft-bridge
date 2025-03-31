// Reference
// https://www.youtube.com/watch?v=d0QktirWbRI
//
oldReceiveMessage2 = receiveMessage2;
oldSendMessage = sendMessage;
receiveMessage2 = function (a) {
    oldReceiveMessage2(a);
    if (!a.startsWith("VU2^") && !a.startsWith("RTA^"))
        console.log("Inbound: " + a);
}
sendMessage = function (a) {
    console.log("Outbound: " + a);
    return oldSendMessage(a);
}