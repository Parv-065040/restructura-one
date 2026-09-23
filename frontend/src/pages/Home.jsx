import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import DepartmentGrid from '../components/DepartmentGrid';
import MethodSection from '../components/MethodSection';
import StackSection from '../components/StackSection';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <div className="min-h-[100dvh]">
      <Navbar />
      <main>
        <Hero />
        <DepartmentGrid />
        <MethodSection />
        <StackSection />
      </main>
      <Footer />
    </div>
  );
}
