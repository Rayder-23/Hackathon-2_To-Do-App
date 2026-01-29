# Data Model: Backend-Frontend Authentication Alignment

## Entities

### JWT Token
- **Fields:**
  - `token` (string): The complete JWT string
  - `header` (dict): JWT header containing algorithm and type
  - `payload` (dict): JWT payload containing claims
  - `signature` (string): JWT signature for verification
- **Validation rules:**
  - Must contain required claims: `sub`, `exp`, `iat`
  - `exp` must be in the future (with 5-second tolerance)
  - `iat` must be reasonable (not too far in the past)
  - `sub` must be a valid user identifier
- **Relationships:** Represents authentication credential issued by Better Auth

### User Identity
- **Fields:**
  - `user_id` (string): Canonical user ID from JWT `sub` claim
  - `authenticated` (boolean): Whether identity has been verified
  - `expires_at` (datetime): When JWT expires
- **Validation rules:**
  - `user_id` must match JWT `sub` claim exactly
  - `authenticated` is true only after successful JWT validation
  - `expires_at` is derived from JWT `exp` claim
- **Relationships:** Derived from verified JWT token, used for authorization decisions

### Authentication Log
- **Fields:**
  - `timestamp` (datetime): When the event occurred
  - `event_type` (string): Type of authentication event (success, failure)
  - `user_id` (string): User ID if available, null for auth failures
  - `ip_address` (string): Client IP address
  - `user_agent` (string): Client user agent string
  - `details` (string): Additional event details
- **Validation rules:**
  - All fields except `user_id` are required
  - `event_type` must be one of: "success", "failure", "error"
- **Relationships:** Records all authentication attempts for security monitoring

## State Transitions

### JWT Token States
```
Unverified → Validating → Valid/Invalid → Processed
```
- Unverified: JWT received from client
- Validating: Signature and claims being validated
- Valid: JWT passed all validation checks
- Invalid: JWT failed validation
- Processed: Final state after request handling

### Authentication Process
```
Request Received → Extract JWT → Validate → Identity Derived → Authorization → Response
```
- Each state has clear success/failure paths
- Failed validation results in immediate termination
- Successful validation leads to authorized request processing

## API Contracts

### Protected Endpoint Requirements
- **Header:** `Authorization: Bearer <JWT_TOKEN>`
- **Validation:** JWT signature, expiration, required claims
- **Identity Extraction:** From `sub` claim in JWT payload
- **Authorization:** Compare JWT `sub` with URL `user_id`

### Error Responses
- **401 Unauthorized:** Invalid/missing JWT, signature failure, expired token
- **403 Forbidden:** Valid JWT but insufficient permissions (user ID mismatch)
- **Response Format:** `{ "detail": "descriptive error message" }`