package com.rick.application.contoller;

import com.rick.application.contoller.excepition.CustomerNotFound;
import com.rick.application.domains.Customer;
import com.rick.application.service.CustomerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.RequestEntity;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/customer")
public class CustomerController {

    @Autowired
    private CustomerService customerService;

    @RequestMapping(method = RequestMethod.POST)
    public ResponseEntity<Void> create(@RequestBody Customer customer){
        customer = customerService.create(customer);

        URI uri = ServletUriComponentsBuilder.fromCurrentRequest().
                path("/{id}").buildAndExpand(customer.getId()).toUri();

        return ResponseEntity.created(uri).build();
    }

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public ResponseEntity<Customer> getByCpf(@RequestParam String cpf){
        Customer customer = null;
        try {
            customer = customerService.readByCpf(cpf);
        } catch (CustomerNotFound e) {
            return ResponseEntity.notFound().build();

        }
        return ResponseEntity.status(HttpStatus.OK).body(customer);
    }


    @RequestMapping(value = "/name", method = RequestMethod.GET)
    public ResponseEntity<List<Customer>> findByNome(@RequestParam("nome")String nome){
        List<Customer> customers = null;
        try {
            customers = customerService.readByNome(nome);
        } catch (CustomerNotFound e){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.status(HttpStatus.OK).body(customers);
    }


    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public ResponseEntity<Customer> find(@PathVariable("id") Long id){
        Customer customer = null;
        try {
            customer = customerService.read(id);
        } catch (CustomerNotFound e) {
            return ResponseEntity.notFound().build();

        }
        return ResponseEntity.status(HttpStatus.OK).body(customer);
    }


    @RequestMapping(method = RequestMethod.GET)
    public ResponseEntity<List<Customer>> listar(){
        return ResponseEntity.status(HttpStatus.OK).body(customerService.listar());
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
    public ResponseEntity<Void> deletar(@PathVariable("id") Long id) {
        try {
            customerService.delete(id);
        } catch (CustomerNotFound e) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.PUT)
    public  ResponseEntity<Void> update(@RequestBody Customer customer, @PathVariable("id") Long id){
        customer.setId(id);
        try {
            customerService.uptade(customer);
        } catch (CustomerNotFound e) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }

}
