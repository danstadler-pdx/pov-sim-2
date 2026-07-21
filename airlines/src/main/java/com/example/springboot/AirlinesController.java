package com.example.springboot;

import java.util.Map;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.client.RestTemplate;

@RestController
@CrossOrigin(origins = "*") // Allow requests from React app
public class AirlinesController {
	private static final String[] airlines = { "AA", "DL", "UA" };

	// Pretty-name lookup, so /airlines/{code}/flights can decorate the
	// downstream flights payload with the human-readable airline.
	private static final Map<String, String> AIRLINE_NAMES = Map.of(
			"AA", "American Airlines",
			"DL", "Delta Air Lines",
			"UA", "United Airlines");

	private final RestTemplate restTemplate;
	private final String flightsServiceUrl;

	public AirlinesController(RestTemplate restTemplate,
			@Value("${FLIGHTS_SERVICE_URL:http://flights:5001}") String flightsServiceUrl) {
		this.restTemplate = restTemplate;
		this.flightsServiceUrl = flightsServiceUrl;
	}

	@Operation(summary = "Index", description = "No-op hello world")
	@GetMapping("/")
	public String index() {
		return "Greetings from Spring Boot!";
	}

	@Operation(summary = "Health check", description = "Performs a simple health check")
	@GetMapping("/health")
	public String health() {
		return "Health check passed!";
	}

	@GetMapping("/airlines")
	@Operation(summary = "Get airlines", description = "Fetch a list of airlines")
	public String getAirlines(
			@Parameter(description = "Optional flag - set raise to true to raise an exception")
			@RequestParam(value = "raise", required = false, defaultValue = "false") boolean raise) {
		if (raise) {
			throw new RuntimeException("Exception raised");
		}
		return String.join(", ", airlines);
	}

	@GetMapping("/airlines/{code}/flights")
	@Operation(summary = "Get flights for an airline",
			description = "Calls the flights service and enriches the response with the airline's human-readable name. "
					+ "Produces a parent-child trace: airlines (server) -> airlines (RestTemplate client) -> flights (server).")
	public Map<String, Object> getFlightsForAirline(
			@PathVariable String code,
			@Parameter(description = "Optional flag - set raise to true to raise an exception")
			@RequestParam(value = "raise", required = false, defaultValue = "false") boolean raise) {
		if (raise) {
			throw new RuntimeException("Exception raised");
		}
		String airlineName = AIRLINE_NAMES.getOrDefault(code, "Unknown");
		String url = flightsServiceUrl + "/flights/" + code;
		Object flightsResponse = restTemplate.getForObject(url, Object.class);
		return Map.of(
				"airline_code", code,
				"airline_name", airlineName,
				"flights_response", flightsResponse);
	}
}
