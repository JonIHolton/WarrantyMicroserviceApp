package ESD.project.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter // Lombok annotation to generate getters
@Setter // Lombok annotation to generate setters
@NoArgsConstructor // Lombok annotation to generate a no-args constructor
@AllArgsConstructor
public class RequestStatusUpdateMessage {
    private int request_Id;
    private String status;
    private String claimee;
    private String email;
}
