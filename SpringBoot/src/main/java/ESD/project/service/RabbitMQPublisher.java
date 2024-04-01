package ESD.project.service;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import ESD.project.model.RequestStatusUpdateMessage;

@Service
public class RabbitMQPublisher {

    @Autowired
    private  RabbitTemplate rabbitTemplate;

    public void publishRequestStatusUpdate(int requestId, String newStatus, String claimee, String email) {
        String exchange = "warranty_service";
        String routingKey = "warranty.update";

        RequestStatusUpdateMessage message = new RequestStatusUpdateMessage(requestId, newStatus, claimee, email);

        rabbitTemplate.convertAndSend(exchange, routingKey, message);
    }
}
