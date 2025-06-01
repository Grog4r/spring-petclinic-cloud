package org.springframework.samples.petclinic.appointments.web.mapper;

public interface Mapper<R, E> {
    E map(E response, R request);
}
