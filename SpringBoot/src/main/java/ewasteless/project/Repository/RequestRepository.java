package ewasteless.project.Repository;
import ewasteless.project.classes.Request;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface RequestRepository extends JpaRepository<Request, Integer> {

    List<Request> findByNameAndRequestId(String name, int requestId);
}

