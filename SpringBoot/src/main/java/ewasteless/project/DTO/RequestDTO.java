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

    private String unitId;

    private String modelId;

    private String modelType;

    private String Claimee;

    private String email;
    
    private String Status;
}
