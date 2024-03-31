package ewasteless.project.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// Correct the import for your Request class
import ewasteless.project.classes.Request;

import ewasteless.project.service.RequestService;
import ewasteless.project.DTO.RequestDTO;

import java.util.List;

@RestController
@RequestMapping("/requests")
public class RequestController {

    @Autowired
    private RequestService requestService;

    @PostMapping
    public ResponseEntity<String> addRequest(@RequestBody RequestDTO requestDTO) {
        try {
            // Assuming addRequest returns the ID of the newly added request
            String requestId = Integer.toString(requestService.addRequest(requestDTO.getModelId(),
                                                         requestDTO.getUnitId(),
                                                         requestDTO.getModelType(),
                                                         requestDTO.getClaimee(),
                                                         requestDTO.getEmail()
                                                        ));

            return ResponseEntity.ok("Request added with ID: " + requestId);
        } catch (Exception e) {
            // Simplified the catch block to catch all exceptions
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error while adding Request: " + e.getMessage());
        }
    }

    @GetMapping("/{requestId}")
    public ResponseEntity<Request> getRequest(@PathVariable int requestId) {
        try {
            Request request = requestService.getRequestById(requestId);
            return ResponseEntity.ok(request);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/all")
    public ResponseEntity<List<Request>> getAllRequests() {
        List<Request> requests = requestService.getAllRequests();
        return ResponseEntity.ok(requests);
    }


    @DeleteMapping("/{requestId}")
    public ResponseEntity<Void> deleteRequest(@PathVariable int requestId) {
        try {
            requestService.deleteRequest(requestId);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}

