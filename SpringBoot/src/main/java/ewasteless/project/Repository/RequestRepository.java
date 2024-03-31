package ewasteless.project.repository;
import org.springframework.data.jpa.repository.JpaRepository;

import org.springframework.stereotype.Repository;

import ewasteless.project.model.Request;


@Repository
public interface RequestRepository extends JpaRepository<Request, Integer> {

}

    