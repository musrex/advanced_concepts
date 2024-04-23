import grpc
import quadratic_pb2
import quadratic_pb2_grpc

def run():
    a = float(input("Enter the coefficient a: "))
    b = float(input("Enter the coefficient b: "))
    c = float(input("Enter the coefficient c: "))

    channel = grpc.insecure_channel("localhost:50051")
    stub = quadratic_pb2_grpc.QuadraticSolverStub(channel)
    response = stub.SolveQuadratic(quadratic_pb2.QuadraticRequest(a=a, b=b, c=c))
    print("Response:", response.solution)

if __name__ == "__main__":
    run()

