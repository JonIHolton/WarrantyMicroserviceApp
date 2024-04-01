package ewasteless.project.DTO;


import com.fasterxml.jackson.annotation.JsonProperty;


import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;


@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class RequestDTO {

    private String unit_Id;

    private String model_Id;

    private String model_Type;

    private String claimee;

    private String email;

    private String description;
    
    private String status;
}
