package com.rick.application.service;

import com.rick.application.contoller.excepition.CustomerNotFound;
import com.rick.application.domains.Customer;
import com.rick.application.repository.CustomerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CustomerService {

    @Autowired
    private CustomerRepository customerRepository;

    public Customer create(Customer customer){
        customer.setId(null);
        return customerRepository.save(customer);
    }

    public Customer read(Long id){
        Customer customer = customerRepository.findById(id).get();

        if(customer == null) {
            throw new CustomerNotFound("o clinte não foi encontrado!");
        }

        return customer;
    }

    public List<Customer> listar(){
        return  customerRepository.findAll();
    }

    public Customer readByCpf(String cpf){
        Customer customer = customerRepository.findByCpf(cpf);

        if(customer == null) {
            throw new CustomerNotFound("customer not found");
        }

        return customer;
    }

    public List<Customer> readByNome(String nome){
        List<Customer> customer = customerRepository.findByNomeWith(nome);

        if(customer == null) {
            throw new CustomerNotFound("customer not found");
        }

        return customer;
    }

    public void delete(Long id) {
        try {
            customerRepository.deleteById(id);
        } catch (EmptyResultDataAccessException e) {
            throw new CustomerNotFound("customer not found");
        }
    }

    public void uptade(Customer customer){
        checkExist(customer);
        customerRepository.save(customer);

    }

    private void checkExist(Customer customer) {
        read(customer.getId());
    }

}
