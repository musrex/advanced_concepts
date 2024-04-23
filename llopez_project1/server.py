import grpc
from concurrent import futures
import quadratic_pb2
import quadratic_pb2_grpc

class QuadraticSolverServicer(quadratic_pb2_grpc.QuadraticSolverServicer):
    def SolveQuadratic(self, request, context):
        a = request.a
        b = request.b
        c = request.c

        discriminant = b**2 - 4*a*c

        if discriminant > 0:
            root1 = (-b + discriminant ** 0.5) / (2 * a)
            root2 = (-b - discriminant ** 0.5) / (2 * a)
            solution = f"Roots are real and distinct: {root1}, {root2}"
        elif discriminant == 0:
            root = -b / (2 * a)
            solution = f"Roots are real and equal: {root}"
        else:
            realPart = -b / (2 * a)
            imaginaryPart = (-discriminant) ** 0.5 / (2 * a)
            solution = f"Roots are complex: {realPart} + {imaginaryPart}i, {realPart} - {imaginaryPart}i"
        
        return quadratic_pb2.QuadraticResponse(solution=solution)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    quadratic_pb2_grpc.add_QuadraticSolverServicer_to_server(QuadraticSolverServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

