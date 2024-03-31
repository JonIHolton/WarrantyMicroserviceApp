package ewasteless.project.service;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


import ewasteless.project.Repository.RequestRepository;
// Model imports
import ewasteless.project.classes.Request;

// Java imports

import java.util.List;

@Service
public class RequestService {

    @Autowired
    private RequestRepository requestRepository;

    public int addRequest(String unitId,           
                            String modelId,             
                            String modelType,
                            String claimee,
                            String email) {
        // Create a Request object
        Request request = new Request(unitId, modelId, modelType, claimee, email);
        request.setStatus("Pending");

        // Save the Request object to the database
        Request savedRequest = requestRepository.save(request);

        // Return the auto-generated request ID
        return savedRequest.getRequestId();
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
