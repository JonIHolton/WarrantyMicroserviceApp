package ewasteless.project.classes;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import java.time.LocalDateTime;
import org.hibernate.annotations.CreationTimestamp;

import jakarta.persistence.Entity;

import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;



@Getter // Lombok annotation to generate getters
@Setter // Lombok annotation to generate setters
@NoArgsConstructor // Lombok annotation to generate a no-args constructor
@Entity // Marks this class as an entity
public class Request {

    @Id // Marks this field as the primary key
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Auto-generation strategy
    private int requestId;

    private String unitId;
    private String modelId;
    private String modelType;
    private String Claimee;
    private String email;
    private String Status;

    @CreationTimestamp // Automatically sets this field when the entity is persisted
    private LocalDateTime createdTimestamp;

    public Request(String unitId, String modelId, String modelType, String claimee, String email) {
        this.unitId = unitId;
        this.modelId = modelId;
        this.modelType = modelType;
        this.Claimee = claimee;
        this.email = email;
    }
}

