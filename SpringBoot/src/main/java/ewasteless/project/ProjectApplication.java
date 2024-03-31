package ewasteless.project;

import java.util.concurrent.ExecutionException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;




@SpringBootApplication
@EnableJpaRepositories(basePackages = "ewasteless.project.repository")
public class ProjectApplication {

	public static void main(String[] args) throws InterruptedException, ExecutionException {
        
		SpringApplication.run(ProjectApplication.class, args);

       
	}
}

