package ewasteless.project.service;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import ewasteless.project.model.Request;
import ewasteless.project.repository.RequestRepository;

// Java imports

import java.util.List;

@Service
public class RequestService {

    @Autowired
    private RequestRepository requestRepository;

    public int addRequest(String unit_Id,           
                            String model_Id,             
                            String model_Type,
                            String claimee,
                            String email,
                            String description) {
        // Create a Request object
        Request request = new Request(unit_Id, model_Id, model_Type, claimee, email, description);
        request.setStatus("Pending");

        // Save the Request object to the database
        Request savedRequest = requestRepository.save(request);

        // Return the auto-generated request ID
        return savedRequest.getRequest_Id();
    }

    public void updateRequestStatus(int requestId, String newStatus) {
        requestRepository.updateStatus(requestId, newStatus);
    }


    public Request getRequestById(int requestId) {
        return requestRepository.findById(requestId)
                .orElseThrow(() -> new RuntimeException("Request not found with id " + requestId));
    }

    public List<Request> getAllRequests() {
        return requestRepository.findAll();
    }


    public void deleteRequest(int requestId) {
        requestRepository.deleteById(requestId);
    }
}
