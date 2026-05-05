import { ShieldX, Home, ArrowLeft } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

/**
 * ForbiddenPage - 403 Error Page
 * 
 * Hiển thị khi user không có quyền truy cập trang
 */
export default function ForbiddenPage() {
    const navigate = useNavigate()

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 p-6 font-sans">
            {/* Background Decorative Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
                <div className="absolute -top-[20%] -left-[10%] w-[500px] h-[500px] bg-red-600/20 rounded-full blur-[120px]" />
                <div className="absolute bottom-[0%] right-[0%] w-[400px] h-[400px] bg-orange-600/20 rounded-full blur-[100px]" />
            </div>

            {/* Content */}
            <div className="relative z-10 text-center max-w-md">
                {/* Icon */}
                <div className="flex justify-center mb-6">
                    <div className="w-24 h-24 bg-red-500/10 rounded-2xl flex items-center justify-center border border-red-500/20">
                        <ShieldX size={48} className="text-red-500" />
                    </div>
                </div>

                {/* Error Code */}
                <h1 className="text-8xl font-black text-white mb-4 tracking-tight">
                    403
                </h1>

                {/* Title */}
                <h2 className="text-2xl font-bold text-white mb-3">
                    Truy Cập Bị Từ Chối
                </h2>

                {/* Description */}
                <p className="text-slate-400 mb-8 leading-relaxed">
                    Bạn không có quyền truy cập trang này. Vui lòng liên hệ quản trị viên nếu bạn cho rằng đây là lỗi.
                </p>

                {/* Actions */}
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                    <button
                        onClick={() => navigate(-1)}
                        className="flex items-center justify-center gap-2 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-semibold transition-all"
                    >
                        <ArrowLeft size={18} />
                        Quay Lại
                    </button>

                    <Link
                        to="/"
                        className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-semibold transition-all"
                    >
                        <Home size={18} />
                        Về Trang Chủ
                    </Link>
                </div>

                {/* Additional Info */}
                <div className="mt-8 p-4 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-xl">
                    <p className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-2">
                        Thông Tin Hỗ Trợ
                    </p>
                    <p className="text-sm text-slate-400">
                        Nếu bạn cần quyền truy cập, vui lòng liên hệ với quản trị viên hệ thống hoặc bộ phận HR.
                    </p>
                </div>
            </div>
        </div>
    )
}
