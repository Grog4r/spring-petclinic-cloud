package org.springframework.samples.petclinic.appointments.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.samples.petclinic.appointments.model.Appointment;
import org.springframework.samples.petclinic.appointments.model.AppointmentRepository;
import org.springframework.samples.petclinic.appointments.web.mapper.AppointmentMapper;
import org.springframework.web.bind.annotation.*;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/appointments")
public class AppointmentResource {

    private final AppointmentRepository repository;

    @Autowired
    public AppointmentResource(AppointmentRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<AppointmentDetails> getAll() {
        return repository.findAll().stream()
                .map(AppointmentMapper::toDetails)
                .collect(Collectors.toList());
    }

    // NEUER ENDPUNKT FÜR POD-INFORMATIONEN
    @GetMapping("/info")
    public ResponseEntity<String> getPodInfo() {
        try {
            String hostname = InetAddress.getLocalHost().getHostName();
            return ResponseEntity.ok("Handled by Pod: " + hostname);
        } catch (UnknownHostException e) {
            return ResponseEntity.status(500).body("Could not determine hostname.");
        }
    }

    @PostMapping("/new")
    public ResponseEntity<AppointmentDetails> create(@RequestBody AppointmentRequest request) {
        Appointment appointment = AppointmentMapper.toEntity(request);
        Appointment saved = repository.save(appointment);
        return ResponseEntity.ok(AppointmentMapper.toDetails(saved));
    }
}
