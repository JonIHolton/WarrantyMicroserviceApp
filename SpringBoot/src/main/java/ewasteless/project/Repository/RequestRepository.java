package ewasteless.project.repository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import ewasteless.project.model.Request;


@Repository
public interface RequestRepository extends JpaRepository<Request, Integer> {
    @Modifying
    @Transactional
    @Query("UPDATE Request r SET r.status = ?2 WHERE r.id = ?1")
    void updateStatus(int requestId, String newStatus);
}

    