package ESD.project.model;

import java.io.Serializable;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter // Lombok annotation to generate getters
@Setter // Lombok annotation to generate setters
@NoArgsConstructor // Lombok annotation to generate a no-args constructor
@AllArgsConstructor
public class RequestStatusUpdateMessage implements Serializable {
    @JsonProperty("request_Id")
    private int request_Id;
    private String status;
    private String claimee;
    private String email;
}



// public class RequestStatusUpdateMessage implements Serializable {
//     private int request_Id;
//     private String newStatus;
//     private String claimee;
//     private String email;
// }


// public record RequestStatusUpdateMessage(@JsonProperty("request_Id") int request_Id,
//                             @JsonProperty("newStatus") String newStatus,
//                             @JsonProperty("claimee") String claimee,
//                             @JsonProperty("email") String email)
//         implements Serializable {
// }